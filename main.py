import streamlit as st

import restaurants

# st.set_page_config(page_title="Page Title", layout="wide")

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

st.title("DGTV")

st.write("Some text")

col1, col2, col3 = st.columns([2, 10, 3])

with col1:
    st.write("Column 1")
    st.write("More text")

with col2:
    st.write("Column 2")
    st.write("More text")

with col3:
    restaurants.widget()
