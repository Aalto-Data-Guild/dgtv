import os

import pandas as pd
import requests
import requests_cache
import streamlit as st

API_URL = os.getenv("KESAKUNTOON_API_URL")

session = requests_cache.CachedSession('kesakuntoon_cache', expire_after=60)


def fetch_data():
    response = session.get(API_URL)
    response.raise_for_status()
    return response.json()


def get_sections(data):
    return [
        ("Average / Total points", pd.DataFrame(data.get("Average / Total points", []))),
        ("Participants", pd.DataFrame(data.get("Participants", []))),
        ("Top 3 Guilds per Category (total points)",
         data.get("Top 3 Guilds per Category (total points)", "No data available")),
        ("Exercise", pd.DataFrame(data.get("Exercise", []))),
        ("Sports Sessions Participation", pd.DataFrame(data.get("Sports Sessions Participation", []))),
        ("Trying New Sports", pd.DataFrame(data.get("Trying New Sports", []))),
        ("Health Points", pd.DataFrame(data.get("Health Points", []))),
    ]


def update_section_index(sections):
    if 'section_index' not in st.session_state:
        st.session_state.section_index = 0

    st.session_state.section_index = (st.session_state.section_index + 1) % len(sections)

    title, content = sections[st.session_state.section_index]
    if isinstance(content, pd.DataFrame) and content.empty:
        st.session_state.section_index = (st.session_state.section_index + 1) % len(sections)
        st.rerun()
    if not isinstance(content, pd.DataFrame) and (content == "No data available" or content == []):
        st.session_state.section_index = (st.session_state.section_index + 1) % len(sections)
        st.rerun()
    return title, content


def display_content(title, content):
    st.markdown(f'### {title}')
    section_container = st.empty()
    with section_container:
        if isinstance(content, pd.DataFrame) and not content.empty:
            if title == "Participants":
                st.bar_chart(content.set_index('name')['value'])
            else:
                styled_content = content.style.map(
                    lambda x: 'font-weight: bold' if x == 'DG' else ''
                ).format(precision=1)
                st.table(styled_content)
        elif not isinstance(content, pd.DataFrame) and content != "No data available" and content != []:
            st.write(content)


def widget():
    st.markdown('## Kesäkuntoon')

    try:
        data = fetch_data()
        sections = get_sections(data)
        title, content = update_section_index(sections)
        display_content(title, content)

    except requests.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
