"""
Weather Data Collector for OneHealth Nexus
Queries Open-Meteo Historical Archive API for surveillance coordinates and stores normalized records.
"""
import os
import requests
import pandas as pd

LOCATIONS = [
    {"name": "Kerala", "lat": 10.8505, "lon": 76.2711, "country": "India"},
    {"name": "Maharashtra", "lat": 19.7515, "lon": 75.7139, "country": "India"},
    {"name": "Delhi", "lat": 28.7041, "lon": 77.1025, "country": "India"},
    {"name": "West Bengal", "lat": 22.9868, "lon": 87.8550, "country": "India"},
    {"name": "Karnataka", "lat": 15.3173, "lon": 75.7139, "country": "India"},
    {"name": "Tamil Nadu", "lat": 11.1271, "lon": 78.6569, "country": "India"},
    {"name": "Assam", "lat": 26.2006, "lon": 92.9376, "country": "India"},
    {"name": "Guangdong", "lat": 23.1291, "lon": 113.2644, "country": "China"},
    {"name": "Cairo", "lat": 30.0444, "lon": 31.2357, "country": "Egypt"},
    {"name": "Jakarta", "lat": -6.2088, "lon": 106.8456, "country": "Indonesia"}
]

def fetch_weather(lat, lon, start_date="2023-01-01", end_date="2023-12-31"):
    # archive endpoint provides historical daily records without api keys
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&"
        f"daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum&timezone=auto"
    )
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json().get("daily", {})

def collect_surveillance_weather(output_path="data/processed/weather_data.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rows = []
    print("Collecting environmental weather observations from Open-Meteo...")
    for loc in LOCATIONS:
        try:
            print(f"  Fetching {loc['name']} ({loc['lat']}, {loc['lon']})...")
            daily = fetch_weather(loc["lat"], loc["lon"])
            dates = daily.get("time", [])
            t_max = daily.get("temperature_2m_max", [])
            t_min = daily.get("temperature_2m_min", [])
            t_mean = daily.get("temperature_2m_mean", [])
            precip = daily.get("precipitation_sum", [])

            for d, mx, mn, me, pr in zip(dates, t_max, t_min, t_mean, precip):
                rows.append({
                    "location": loc["name"],
                    "country": loc["country"],
                    "latitude": loc["lat"],
                    "longitude": loc["lon"],
                    "date": d,
                    "temperature_max_c": mx,
                    "temperature_min_c": mn,
                    "temperature_mean_c": me,
                    "precipitation_mm": pr,
                    "source": "Open-Meteo Archive API"
                })
        except Exception as e:
            print(f"  Warning: failed to fetch for {loc['name']}: {e}")

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} weather records to {output_path}")
    return df

if __name__ == "__main__":
    df = collect_surveillance_weather()
    assert len(df) > 0, "Weather collection produced empty dataframe"
    print("Self-check passed: Weather data collected and validated.")

