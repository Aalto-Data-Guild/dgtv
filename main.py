import streamlit as st

import restaurants
import weather

st.set_page_config(page_title="DGTV", layout="wide", page_icon="📺")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.markdown("# DGTV")

col1, col2, col3 = st.columns([2, 4, 4])

with col1:
    weather.widget()

with col2:
    st.markdown("## Column 2")
    st.write("More text")

with col3:
    restaurants.widget()
