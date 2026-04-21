import os
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
import requests

BASE_URL = "https://api.waqi.info/feed"
API_TOKEN = "2767aa8903e54e7d0780b349eb51133dc258df78"


def fetch_aqi(city: str) -> Dict:
    """
    Fetch real-time AQI data for a given city.
    Returns a clean dictionary containing AQI, timestamp, and pollutant values.
    """
    if not API_TOKEN:
        raise ValueError("API token not found. Please set WAQI_API_TOKEN.")

    if not city or not city.strip():
        return {}

    url = f"{BASE_URL}/{city.strip()}/?token={API_TOKEN}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        raw = response.json()
    except requests.exceptions.RequestException:
        return {}
    except ValueError:
        return {}

    if raw.get("status") != "ok":
        return {}

    data = raw.get("data", {})
    iaqi = data.get("iaqi", {})

    aqi_raw = data.get("aqi")
    aqi_value = safe_int(aqi_raw)

    return {
        "city": data.get("city", {}).get("name", city.title()),
        "aqi": aqi_value,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pollutants": {
            "pm25": get_pollutant_value(iaqi, "pm25"),
            "pm10": get_pollutant_value(iaqi, "pm10"),
            "co": get_pollutant_value(iaqi, "co"),
            "no2": get_pollutant_value(iaqi, "no2"),
            "o3": get_pollutant_value(iaqi, "o3"),
            "so2": get_pollutant_value(iaqi, "so2"),
        },
    }


def fetch_multiple_cities(cities: List[str]) -> List[Dict]:
    """
    Fetch AQI data for multiple cities.
    Returns a list of AQI dictionaries.
    """
    results = []
    for city in cities:
        data = fetch_aqi(city)
        if data:
            results.append(data)
    return results


def get_pollutant_value(iaqi: Dict, key: str) -> Optional[float]:
    """
    Safely get pollutant value from API response.
    """
    value = iaqi.get(key, {}).get("v")
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def safe_int(value) -> Optional[int]:
    """
    Convert a value to int safely.
    """
    try:
        if value is None:
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def to_dataframe(aqi_list: List[Dict]) -> pd.DataFrame:
    """
    Convert a list of AQI dictionaries into a pandas DataFrame.
    """
    rows = []
    for entry in aqi_list:
        pollutants = entry.get("pollutants", {})
        row = {
            "City": entry.get("city"),
            "AQI": entry.get("aqi"),
            "Status": get_aqi_status(entry.get("aqi")),
            "Timestamp": entry.get("timestamp"),
            "PM2.5": pollutants.get("pm25"),
            "PM10": pollutants.get("pm10"),
            "CO": pollutants.get("co"),
            "NO2": pollutants.get("no2"),
            "O3": pollutants.get("o3"),
            "SO2": pollutants.get("so2"),
        }
        rows.append(row)

    return pd.DataFrame(rows)


def get_aqi_status(aqi: Optional[int]) -> str:
    """
    Return AQI category label based on AQI value.
    """
    if aqi is None:
        return "Unavailable"
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
    return "Hazardous ⚫"


def get_health_advice(aqi: Optional[int]) -> str:
    """
    Return health advice based on AQI value.
    """
    if aqi is None:
        return "Air quality data is unavailable right now."
    if aqi <= 50:
        return "Air quality is great. Safe for outdoor activities."
    elif aqi <= 100:
        return "Air quality is acceptable. Sensitive people should reduce prolonged outdoor activity."
    elif aqi <= 150:
        return "Sensitive groups should reduce outdoor activities."
    elif aqi <= 200:
        return "Everyone should limit outdoor activities. Consider wearing a mask outside."
    elif aqi <= 300:
        return "Avoid outdoor activities. Keep windows closed if possible."
    return "Emergency-level pollution. Stay indoors and avoid outdoor exposure."


def get_aqi_color(aqi: Optional[int]) -> str:
    """
    Return a color name for AQI category.
    """
    if aqi is None:
        return "gray"
    if aqi <= 50:
        return "green"
    elif aqi <= 100:
        return "yellow"
    elif aqi <= 150:
        return "orange"
    elif aqi <= 200:
        return "red"
    elif aqi <= 300:
        return "purple"
    return "maroon"
