import requests
from datetime import datetime

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather(latitude, longitude):
    try:
        lat = float(latitude)
        lon = float(longitude)
    except (TypeError, ValueError):
        print("Invalid coordinates: must be numeric.")
        return None

    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        print("Coordinates out of range.")
        return None

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "timezone": "auto"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        print("Connection error: check your internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return None
    except requests.RequestException as e:
        print("Request failed:", e)
        return None

    current = data.get("current")
    if not current:
        print("No current data found in response:", data)
        return None

    return {
        "latitude": lat,
        "longitude": lon,
        "temperature": current.get("temperature_2m"),
        "weather_code": current.get("weather_code"),
        "wind_speed": current.get("wind_speed_10m"),
        "timestamp": current.get("time", datetime.utcnow().isoformat())
    }


if __name__ == "__main__":
    # Example: London
    result = get_weather(51.5074, -0.1278)
    if result:
        print("Weather data:", result)
    else:        print("Failed to retrieve weather data.")