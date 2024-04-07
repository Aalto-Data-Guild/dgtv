import streamlit as st
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def widget():
    st.markdown("## Weather")
    weather_data = get_weather_data()
    for data in weather_data:
        st.markdown(data)

def get_weather_data():
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 60.184,
        "longitude": 24.8279,
        "current": ["temperature_2m", "weather_code"],
        "timezone": "auto",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_weather_code = current.Variables(1).Value()

    return [current_temperature_2m, current_weather_code]