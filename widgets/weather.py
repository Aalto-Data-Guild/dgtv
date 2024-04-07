import streamlit as st
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def widget():
    st.markdown("## Weather")
    weather_data = get_weather_data()

    st.markdown("### Forecast")
    forecast_chart_data = weather_data.rename(columns = {'date':'Time', 'temperature':'Temperature', 'precipitation':'Precipitation'})
    st.line_chart(data = forecast_chart_data, x = 'Time', y = ['Temperature', 'Precipitation'], color = ['#63b8ff', '#ff4500'])

def get_weather_data():
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 60.184,
        "longitude": 24.8279,
        "hourly": ["temperature_2m", "precipitation", "weather_code"],
        "timezone": "auto",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature"] = hourly_temperature_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["weather_code"] = hourly_weather_code

    hourly_dataframe = pd.DataFrame(data = hourly_data)

    return hourly_dataframe