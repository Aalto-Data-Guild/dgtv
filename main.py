import time
import streamlit as st
import ui
import os

from widgets import WeatherWidget, RestaurantsWidget, CountdownToWappuWidget, EventsWidget

# Setting up the page
st.set_page_config(page_title="DGTV", layout="wide", page_icon="📺")

# some streamlit fluff is removed through config.toml
ui.add_logo()
ui.remove_header()
ui.add_footer()
ui.remove_container_padding()

ui.update_font_size()

# single element container to ensure the dashboard gets updated
main_container = st.empty()

def init_widgets():
    return {
        'weather': WeatherWidget(),
        'restaurants': RestaurantsWidget(),
        'countdown_to_wappu': CountdownToWappuWidget(os.getenv('WAPPU_ANNOUNCED', 'false').lower() == 'true'),
        'events': EventsWidget(os.getenv('EVENTS_API_URL', 'https://events.dataguild.fi/api/events')),
    }

widgets = init_widgets()

def get_visible_widgets():
    return [widget for widget in widgets.values() if widget.is_visible]

while True:
    visible_widgets = get_visible_widgets()
    with main_container:
        cols = st.columns([2]*len(visible_widgets), gap='medium')
        for col, widget in zip(cols, visible_widgets):
            with col:
                widget.render()
    time.sleep(1)

