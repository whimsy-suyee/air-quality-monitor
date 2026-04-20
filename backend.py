import requests
import pandas as pd
from datetime import datetime

API_TOKEN = "2767aa8903e54e7d0780b349eb51133dc258df78"
BASE_URL = "https://api.waqi.info/feed"


# 1. FETCH REAL-TIME AQI DATA (Data Structure - Dictionary)
def fetch_aqi(city: str) -> dict:
    """
    Fetch real-time AQI data for a given city.
    Returns a dictionary with AQI and pollutant values.
    """
    url = f"{BASE_URL}/{city}/?token={API_TOKEN}"
    response = requests.get(url)
    raw = response.json()

    if raw["status"] != "ok":
        return {}

    data = raw["data"]

    # FIX AQI VALUE
    aqi_raw = data.get("aqi")
    aqi_value = None

    if isinstance(aqi_raw, int):
        aqi_value = aqi_raw
    elif isinstance(aqi_raw, str) and aqi_raw.isdigit():
        aqi_value = int(aqi_raw)

    # Store in a clean dictionary (Data Structure)
    return {
        "city": city,
        "aqi": aqi_value,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pollutants": {
            "pm25": data["iaqi"].get("pm25", {}).get("v", None),
            "pm10": data["iaqi"].get("pm10", {}).get("v", None),
            "co":   data["iaqi"].get("co",   {}).get("v", None),
            "no2":  data["iaqi"].get("no2",  {}).get("v", None),
            "o3":   data["iaqi"].get("o3",   {}).get("v", None),
        }
    }

# 2. FETCH MULTIPLE CITIES (Data Structure - List of Dicts)
    """
    Fetch AQI data for multiple cities.
    Returns a list of dictionaries.
    """
def fetch_multiple_cities(cities: list) -> list:
    results = []
    for city in cities:
        data = fetch_aqi(city)
        if data:
            results.append(data)
    return results

# 3. CONVERT TO PANDAS DATAFRAME (Data Manipulation)

def to_dataframe(aqi_list: list) -> pd.DataFrame:
    rows = []
    for entry in aqi_list:
        row = {
            "City": entry["city"],
            "AQI": entry["aqi"],
            "Timestamp": entry["timestamp"],
            "PM2.5": entry["pollutants"]["pm25"],
            "PM10": entry["pollutants"]["pm10"],
            "CO": entry["pollutants"]["co"],
            "NO2": entry["pollutants"]["no2"],
            "O3": entry["pollutants"]["o3"],
        }
        rows.append(row)

    return pd.DataFrame(rows)

# 4. AQI HEALTH STATUS LABEL
    """
    Returns health status label based on AQI value.
    """
def get_aqi_status(aqi: int) -> str:
    if aqi <= 50:
        return "Good 🟢"
    elif aqi <= 100:
        return "Moderate 🟡"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups 🟠"
    elif aqi <= 200:
        return "Unhealthy 🔴"
    elif aqi <= 300:
        return "Very Unhealthy 🟣"
    else:
        return "Hazardous ⚫"

# 5. HEALTH ADVICE
def get_health_advice(aqi: int) -> str:
    if aqi <= 50:
        return "Air quality is great! Safe for outdoor activities."
    elif aqi <= 100:
        return "Acceptable air quality. Sensitive people should limit prolonged outdoor exposure."
    elif aqi <= 150:
        return "Sensitive groups should reduce outdoor activities."
    elif aqi <= 200:
        return "Everyone should limit outdoor activities. Wear a mask if going outside."
    elif aqi <= 300:
        return "Avoid outdoor activities. Keep windows closed."
    else:
        return "Emergency conditions. Stay indoors and avoid all outdoor exposure!"