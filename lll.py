import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)
locations = [
    {"name": "Oran", "lat": 35.6991, "lon": -0.6359},
    {"name": "Algiers", "lat": 36.7525, "lon": 3.04197},
]

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": [loc["lat"] for loc in locations],
    "longitude": [loc["lon"] for loc in locations],
    "hourly": ["wind_speed_10m", "wind_gusts_10m", "pressure_msl"],
    "forecast_days": 7,
    "timezone": "auto"
}

responses = openmeteo.weather_api(url, params=params)

all_rows = []

for i, response in enumerate(responses):
    city = locations[i]["name"]

    hourly = response.Hourly()

    wind_speed = hourly.Variables(0).ValuesAsNumpy()
    wind_gusts = hourly.Variables(1).ValuesAsNumpy()
    pressure = hourly.Variables(2).ValuesAsNumpy()

    dates = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s"),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )

    for d, ws, wg, p in zip(dates, wind_speed, wind_gusts, pressure):
        all_rows.append({
            "datetime": d,
            "city": city,
            "wind_speed_10m": float(ws),
            "wind_gusts_10m": float(wg),
            "pressure_msl": float(p)
        })


df_all = pd.DataFrame(all_rows)

# ================== SAVE TO ONE EXCEL FILE ==================
df_all.to_excel("weather_hourly_all.xlsx", index=False)

print(" SUCCESS: File created -> weather_hourly_all.xlsx")
print(df_all.head())

