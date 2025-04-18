import time

import streamlit as st

import ui
from widgets import restaurants, weather, kesakuntoon, countdownToWappu

# Setting up the page
st.set_page_config(page_title="DGTV", layout="wide", page_icon="📺")

# some streamlit fluff is removed through config.toml
ui.add_logo()
ui.remove_header()
ui.remove_container_padding()

ui.update_font_size()

# single element container to ensure the dashboard gets updated
main_container = st.empty()

while True:
    # *data update logic* ?

    with main_container:
        # column widths can be adjusted later
        col1, col2, col3, col4 = st.columns([2, 2, 4, 2], gap='medium')

        with col1:
            weather.widget()

        with col3:
            restaurants.widget()

        with col4:
            countdownToWappu.widget()

    time.sleep(1)
