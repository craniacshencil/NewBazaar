import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import base64
from st_clickable_images import clickable_images


#Check Login Status
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authentication_status = st.session_state["authentication_status"]
name = st.session_state["name"]

if not authentication_status:
    switch_page("Login")

# Remove sidebar,adding header image
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
st.columns(3)[1].image("images\\header.png" ,use_column_width="auto")

#Nav bar setup
nav_bar = option_menu(None, ["Home", "Check Valuation", "My Listings", "Wishlist"],
    icons=["Home", 'cash-coin', "car-front", "bag-heart-fill"],
    menu_icon="cast", default_index = 0, orientation="horizontal")
if nav_bar == "Check Valuation":
	switch_page("valuation")

if nav_bar == "My Listings":
	switch_page("mylisting")

if nav_bar == "Wishlist":
	switch_page("wishlist")

#Content
col1, col2 = st.columns([0.05, 0.95])
with col2:
    images = []
    for file in ["images//buy_now.png", "images//sell_ride.png"]:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")

    clicked = clickable_images(
        images,
        titles = ["buy", "sell"],
        div_style = {"display": "block", "justify-content": "flex-start", "flex-wrap": "nowrap", "width" : "1200px"},
        img_style = {"margin": "1px", "height": "590px", "width" : "590px"},
    )
    if clicked == 0:
          switch_page("listings")
    if clicked == 1:
          switch_page("valuation")

