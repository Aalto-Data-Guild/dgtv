import altair as alt
import openmeteo_requests
import pandas as pd
import requests_cache
import streamlit as st
from retry_requests import retry
from widgets.base_widget import BaseWidget

class WeatherWidget(BaseWidget):
    name = 'Weather'

    def render(self):
        st.markdown("# Weather")
        current_temperature, current_weather_code, forecast_df = get_weather_data()

        # st.markdown(f'### Current Temperature: **{round(current_temperature, 1)}°C**')
        st.metric(label="Current Temperature", value=f"{round(current_temperature, 1)} °C")

        st.markdown("### Forecast")
        forecast_df = forecast_df.rename(
            columns={'date': 'Time', 'temperature': 'Temperature', 'precipitation': 'Precipitation'})

        base = alt.Chart(forecast_df).encode(
            alt.X('hoursminutes(Time):O', title=None, axis=alt.Axis(labelAngle=-45))
        ).properties(
            height=300, width=600
        )

        COLOR_BLUE = '#00d4ff'
        COLOR_SILVER = '#4ade80'

        line = base.mark_line(color=COLOR_SILVER, point=alt.OverlayMarkDef(color=COLOR_SILVER)).encode(
            alt.Y('Temperature', title='Temperature (°C)', axis=alt.Axis(titleColor=COLOR_SILVER))
        )

        bar = base.mark_bar(color=COLOR_BLUE, opacity=0.6).encode(
            alt.Y('Precipitation', title='Precipitation (mm)', axis=alt.Axis(titleColor=COLOR_BLUE))
        )

        st.altair_chart(alt.layer(line, bar).resolve_scale(y='independent'), use_container_width=True)

def get_weather_data():
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 60.184,
        "longitude": 24.8279,
        "current": ["temperature_2m", "weather_code"],
	    "hourly": ["temperature_2m", "precipitation"],
        "timezone": "Europe/Helsinki",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()
    current_temperature = current.Variables(0).Value()
    current_weather_code = current.Variables(1).Value()

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature"] = hourly_temperature_2m
    hourly_data["precipitation"] = hourly_precipitation

    forecast_df = pd.DataFrame(data = hourly_data)

    return current_temperature, current_weather_code, forecast_df