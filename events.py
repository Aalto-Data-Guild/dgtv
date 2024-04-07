import streamlit as st
import requests as r
from datetime import datetime

def load_events():
    req = r.get('http://dev.dataguild.fi/api/events')
    return req.json()

def widget():
    st.markdown('## Upcoming events:')
    events = load_events()

    for event in events:
        _date = datetime.fromisoformat(event['date'])
        total_signups = sum([quota['signupCount'] for quota in event['quotas']])
        total_seats = sum([quota['size'] for quota in event['quotas']])
        st.write(f"{event['title']} - {_date.strftime('%d/%m %H:%M')} ({total_signups}/{total_seats})")



