import streamlit as st
from datetime import datetime
from widgets.base_widget import BaseWidget

def load_countDown():
    now = datetime.now()
    current_year = now.year
    wappu = datetime(current_year, 5, 1)

    if now > wappu:
        wappu = datetime(current_year + 1, 5, 1)

    time_difference =wappu  - now
    days = time_difference.days
    seconds = time_difference.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if now ==datetime(current_year, 5, 1, ):
        return []

    if days < 30:
        if days>7:
            return [days, hours, minutes]
        else:
            return [days, hours]
    else:
        return [days]

class CountdownToWappuWidget(BaseWidget):
    name = 'Countdown to Wappu'

    def __init__(self, wappuAnnounced=False):
        super().__init__()
        self.wappuAnnounced = wappuAnnounced

    def render(self):
        if not self.wappuAnnounced:
            st.write('## Days until possible  Wappu:')
        else:
            st.markdown('## Days until Wappu:')
        time = load_countDown()
        match len(time):
            case 0:
                st.write("# WABU!")
            case 1:
                st.markdown(f"# {time[0]} days")
            case 2:
                st.markdown(f"# {time[0]} days and {time[1]} hours")
            case 3:
                st.markdown(f"# {time[0]} days, {time[1]} hours and {time[2]} minutes")

    @property
    def is_visible(self):
        ## Visible after March 1st to May 2nd (not any other days of may) or if Wappu is announced
        if self.wappuAnnounced:
            return True
        
        current_date = datetime.now()
        if current_date.month == 5:
            return current_date.day < 2
        return current_date.month >= 3 and current_date.month < 5


