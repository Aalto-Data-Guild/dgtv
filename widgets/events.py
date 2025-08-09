import streamlit as st
import requests as r
from datetime import datetime, timezone
from widgets.base_widget import BaseWidget

def load_events(api_url):
    req = r.get(api_url)
    if req.status_code != 200:
        st.error("Failed to load events. Please try again later.")
        return []
    try:
        return req.json()
    except ValueError:
        st.error("Failed to parse events data. Please check the API.")
        return []

class EventsWidget(BaseWidget):
    name = 'Events'

    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url

    def render(self):
        st.markdown('# Upcoming events')
        events = load_events(self.api_url)

        for event in events:
            _date = datetime.fromisoformat(event['date'])
            if _date.tzinfo is None:
                _date = _date.replace(tzinfo=timezone.utc).astimezone(tz=None)
            total_signups = sum([quota['signupCount'] for quota in event['quotas']])
            total_seats = sum([quota['size'] for quota in event['quotas']])
            st.write(f"### {event['title']} - {_date.strftime('%d.%m %H:%M')}")

            location = event.get('location', None)
            if location:
                st.write(f":material/location_on: {location}")

            if total_seats > 0:
                st.progress(total_signups / total_seats if total_seats > 0 else 0, 
                        text=f"{total_signups}/{total_seats} seats filled")
