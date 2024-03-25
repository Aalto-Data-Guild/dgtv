import time

import streamlit as st

import restaurants
import weather

# Setting up the page
st.set_page_config(page_title="DGTV", layout="wide", page_icon="📺")

# streamlit fluff is removed through config.toml

# logo next to header, vertically aligned
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="https://dataguild.fi/wp-content/uploads/2023/07/dataguild_logo_raster_1280x1120_black_transparent.png" width=64>
        <h1 style="margin: 0; padding-left: 10px;">DGTV</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# single element container to ensure the dashboard gets updated
main_container = st.empty()

while True:
    # *data update logic*

    with main_container:
        # column widths can be adjusted later
        col1, col2, col3 = st.columns([2, 4, 4], gap='medium')

        with col1:
            weather.widget()

        with col2:
            st.markdown("## Column 2")
            st.write(f"Current time&date: {time.strftime('%H:%M:%S %d-%m-%Y')}")

        with col3:
            restaurants.widget()

    time.sleep(1)
