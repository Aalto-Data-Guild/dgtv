import streamlit as st


def update_html(content: str):
    st.markdown(content, unsafe_allow_html=True)


# logo next to header, vertically aligned
def add_logo():
    update_html(
        """
        <div style="display: flex; align-items: center;">
            <img src="https://dataguild.fi/wp-content/uploads/2023/07/dataguild_logo_raster_1280x1120_black_transparent.png" width=64>
            <h1 style="margin: 0; padding-left: 10px; padding-top: 0.9rem;">DGTV</h1>
        </div>   
        """
    )


# remove the sticky header above the logo
def remove_header():
    update_html(
        """
        <style>
            #MainMenu, header, footer {visibility: hidden;}

            /* This code gets the first element on the sidebar,
            and overrides its default styling */
            section[data-testid="stSidebar"] div:first-child {
                top: 0;
                height: 100vh;
            }
        </style>
        """
    )


def remove_container_padding():
    update_html(
        """
        <style>
            div.block-container{
            padding-top:1rem; padding-left:2rem
            }
        </style>
        """
    )
