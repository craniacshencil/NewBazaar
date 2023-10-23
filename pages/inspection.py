import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from yaml.loader import SafeLoader
from streamlit_option_menu import option_menu


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

if (not authentication_status) or (name != "admin2"):
    switch_page("Login")

#Header image and text
st.columns(3)[1].image("images/header.png",use_column_width="auto")

#Adding NavBar
nav_bar = option_menu(None, ["Dashboard", "Ban User", "Schedule Inspection"],
    icons=['house', 'exclamation-diamond', "calendar3"],
    menu_icon = "cast", default_index = 2, orientation = "horizontal")

if nav_bar == "Dashboard":
	switch_page("admin")

if nav_bar == "Ban User":
	switch_page("banuser")

#Header Text
colored_header(
label = "Inspection Schedule",
description = "",
color_name = "red-70",
)