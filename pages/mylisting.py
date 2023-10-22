import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu

from yaml.loader import SafeLoader
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

#Nav bar setup
nav_bar = option_menu(None, ["Home", "Check Valuation", "My Listings", "Wishlist"],
    icons=["Home", 'cash-coin', "car-front", "bag-heart-fill"],
    menu_icon="cast", default_index = 2, orientation="horizontal")
if nav_bar == "Check Valuation":
	switch_page("valuation")

if nav_bar == "Home":
	switch_page("dashboard")

if nav_bar == "Wishlist":
	switch_page("wishlist")

#Content
