import time

import streamlit as st

from widgets import events, restaurants, weather
import ui

# Setting up the page
st.set_page_config(page_title="DGTV", layout="wide", page_icon="📺")

# some streamlit fluff is removed through config.toml
ui.add_logo()
ui.remove_header()
ui.remove_container_padding()

# single element container to ensure the dashboard gets updated
main_container = st.empty()

while True:
    # *data update logic* ?

    with main_container:
        # column widths can be adjusted later
        col1, col2, col3, col4 = st.columns([2, 2, 4, 2], gap='medium')

        with col1:
            weather.widget()

        with col2:
            st.markdown("## Column 2")
            st.write(f"Current time&date: {time.strftime('%H:%M:%S %d-%m-%Y')}")

        with col3:
            restaurants.widget()

        with col4:
            events.widget()

    time.sleep(1)
