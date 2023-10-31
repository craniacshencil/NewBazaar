import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from yaml.loader import SafeLoader
from streamlit_option_menu import option_menu
from pymongo import MongoClient
import pymongo

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

#Logout
colspace, colspace2, column1 = st.columns((8, 10, 2))

with column1:
    if st.session_state["authentication_status"]:
        authenticator.logout(f'{name} Logout', 'main', key='unique_key')

#Header image and text
st.columns(3)[1].image("images/header.png",use_column_width="auto")

#Header Text
colored_header(
label = "User Ban",
description = "",
color_name = "red-70",
)

#Initilazing mongoDb connection
client = MongoClient("localhost", 27017)
db = client.CarBazaar
listings = db.post
wishlists = db.wishlist

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
        listings.delete_many({'Seller' : name})
        wishlists.delete_many({'User' : name})
    else:
        print(f"User '{selected_username}' not found in the list of usernames.")
    # Save the modified data back to the YAML file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)



