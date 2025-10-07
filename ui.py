import streamlit as st


def update_html(content: str):
    st.html(content)


# logo next to header, vertically aligned
def add_logo():
    update_html(
        """
        <div style="display: flex; align-items: center;">
            <img src="https://dataguild.fi/wp-content/uploads/2023/07/dataguild_logo_raster_1280x1120_white_transparent.png" width=64>
            <h1 style="margin: 0; padding-left: 10px; padding-top: 0.9rem;">DGTV</h1>
            <div style="display: flex; align-items: center; padding-left: 10px; column-gap: 2rem; padding-left: 2.5rem">
                <img src="https://dataguild.fi/wp-content/uploads/2024/01/EY.png" height=64 style="margin-right: 1rem" />
                <img src="https://dataguild.fi/wp-content/uploads/2024/01/netlightllogo.png" height=64 />
                <img src="https://dataguild.fi/wp-content/uploads/2024/01/codentologo.png" height=64 />
                <img src="https://dataguild.fi/wp-content/uploads/2024/01/twoday-wordmark-RGB_WHITE.png" height=64 />
            </div>
        </div>
        """
    )

def add_footer():
    update_html(
        """
        <footer style="text-align: center; padding-top: 1rem;">
            <p style="color: #888;">Made with ❤️ by <a href="https://dataguild.fi" style="color: #888;">Data Guild</a> </p>
        </footer>
        <style>
            footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                text-align: center;
                padding: 10px;
            }
        </style> 
        """
    )

# remove the sticky header above the logo
def remove_header():
    update_html(
        """
        <style>
            #MainMenu, header {visibility: hidden;}

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
    
def update_font_size():
    update_html(
        """
        <style>
            div, p {
                font-size: 20px;
            }
        <style>
        """
    )
