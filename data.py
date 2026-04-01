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
        print(f"Error: Could not fetch data for '{city}'")
        return {}

    data = raw["data"]

    # Store in a clean dictionary (Data Structure)
    aqi_data = {
        "city": city,
        "aqi": data.get("aqi", "N/A"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pollutants": {
            "pm25": data["iaqi"].get("pm25", {}).get("v", "N/A"),
            "pm10": data["iaqi"].get("pm10", {}).get("v", "N/A"),
            "co":   data["iaqi"].get("co",   {}).get("v", "N/A"),
            "no2":  data["iaqi"].get("no2",  {}).get("v", "N/A"),
            "o3":   data["iaqi"].get("o3",   {}).get("v", "N/A"),
        }
    }

    return aqi_data


# 2. FETCH MULTIPLE CITIES (Data Structure - List of Dicts)
def fetch_multiple_cities(cities: list) -> list:
    """
    Fetch AQI data for multiple cities.
    Returns a list of dictionaries.
    """
    results = []
    for city in cities:
        print(f"Fetching data for {city}...")
        data = fetch_aqi(city)
        if data:
            results.append(data)
    return results


# 3. CONVERT TO PANDAS DATAFRAME (Data Manipulation)

def to_dataframe(aqi_list: list) -> pd.DataFrame:
    rows = []
    for entry in aqi_list:
        row = {
            "City":      entry["city"],
            # 👈 add this
            "AQI":       entry["aqi"] if entry["aqi"] != "-" else None,
            "Timestamp": entry["timestamp"],
            "PM2.5":     entry["pollutants"]["pm25"],
            "PM10":      entry["pollutants"]["pm10"],
            "CO":        entry["pollutants"]["co"],
            "NO2":       entry["pollutants"]["no2"],
            "O3":        entry["pollutants"]["o3"],
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


# 4. AQI HEALTH STATUS LABEL

def get_aqi_status(aqi: int) -> str:
    """
    Returns health status label based on AQI value.
    """
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


def get_health_advice(aqi: int) -> str:
    """
    Returns health advice based on AQI value.
    """
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


# 5. MAIN TEST
if __name__ == "__main__":
    # Test with a few cities
    cities = ["phnompenh", "bangkok", "singapore"]
    aqi_list = fetch_multiple_cities(cities)

    # Convert to DataFrame
    df = to_dataframe(aqi_list)

    # Print results
    print("\n📊 Air Quality Data:")
    print(df.to_string(index=False))

    # Show AQI status for each city
    print("\n🏥 Health Status:")
for entry in aqi_list:
    aqi_val = entry["aqi"]

    if aqi_val == "-" or aqi_val == "N/A":  # 👈 add this check
        print(f"  {entry['city'].capitalize()} — AQI data not available\n")
        continue

    status = get_aqi_status(aqi_val)
    advice = get_health_advice(aqi_val)
    print(f"  {entry['city'].capitalize()} — AQI: {aqi_val} | {status}")
    print(f"  💡 {advice}\n")
