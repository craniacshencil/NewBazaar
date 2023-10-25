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
    menu_icon = "cast", default_index = 1, orientation = "horizontal")

if nav_bar == "Schedule Inspection":
	switch_page("inspection")

#Header Text
colored_header(
label = "User Ban",
description = "",
color_name = "red-70",
)

#Content

# Load the YAML file
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Extract usernames
usernames = list(config.get('credentials', {}).get('usernames', {}).keys())

# Remove the 'admin2' username if it exists
if 'admin2' in usernames:
    usernames.remove('admin2')

# Select the username you want to delete
selected_username = st.selectbox("Select username of user to ban: ", usernames)

if st.button("Confirm Ban"):
    # Check if the selected username exists in the list
    if selected_username in usernames:
    # Remove the user details associated with the selected username
        del config['credentials']['usernames'][selected_username]
        print(f"User '{selected_username}' has been deleted.")
    else:
        print(f"User '{selected_username}' not found in the list of usernames.")
    # Save the modified data back to the YAML file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)



