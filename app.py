import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

# Collapse sidebar on start, remove it and header image
st.set_page_config(initial_sidebar_state="collapsed",layout="wide")
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
st.columns(3)[1].image("images/header.png",use_column_width="auto")

#Adding NavBar
nav_bar = option_menu(None, ["Home", "Login", "Register"],
    icons=['house', 'cloud-upload', "list-task", 'gear'],
    menu_icon="cast", default_index=0, orientation="horizontal")

if nav_bar == "Login":
	switch_page("login")

if nav_bar == "Register":
	switch_page("register")
	
#Content
col1, col2 = st.columns(2,gap="small")
with col1:
	st.image("images/buy_now.png")
with col2:
	st.image("images/sell_ride.png")
