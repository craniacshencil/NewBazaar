import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
from yaml.loader import SafeLoader

#Check Login status
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

# Remove sidebar via CSS and adding header image
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

#NavBar config
nav_bar = option_menu(None, ["Home", "Check Valuation", "Buy", "My Listings", "Wishlist"],
    icons=["house-fill", 'cash-coin', "car-front", "bag", "bookmark-heart-fill"],
    menu_icon="cast", default_index = 4, orientation="horizontal")
if nav_bar == "Home":
    switch_page("dashboard")
if nav_bar == "My Listings":
    switch_page("mylisting")
if nav_bar == "Check Valuation":
    switch_page("valuation")
if nav_bar == "Buy":
    switch_page("listings")

#Content