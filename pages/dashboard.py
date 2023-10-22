import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

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
col1, col2 = st.columns(2, gap="small")
with col1:
	st.image("images/buy_now.png")

with col2:
	st.image("images/sell_ride.png")

