import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_extras.switch_page_button import switch_page
from streamlit_option_menu import option_menu
import pandas as pd
from streamlit_extras.stylable_container import stylable_container 
import pymongo
from pymongo import MongoClient
from PIL import Image
import pillow_avif
import requests
from io import BytesIO

#Check Login Status
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
#Remove sidebar, add header image
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
st.columns(3)[1].image("images\\header.png",use_column_width="auto")

#NavBar config
nav_bar = option_menu(None, ["Home", "Check Valuation", "Buy", "My Listings", "Wishlist"],
    icons=["house-fill", 'cash-coin', "car-front", "bag", "bookmark-heart-fill"],
    menu_icon="cast", default_index = 2, orientation="horizontal")
if nav_bar == "Home":
    switch_page("dashboard")
if nav_bar == "My Listings":
    switch_page("mylisting")
if nav_bar == "Wishlist":
    switch_page("wishlist")
if nav_bar == "Check Valuation":
    switch_page("valuation")

#MongoDB config
client = MongoClient("localhost", 27017)
db = client.carbazaar
listings = db.post

#Content
st.header("Listings", divider = "red")
lmargin, col1, col2, col3, rmargin = st.columns([0.075, 0.25, 0.25, 0.25, 0.075])

#Adding a session state to transfer information
st.session_state['car'] = None

# #Display before filtering
cars = list(listings.find())
imgs = [car.get('Images') for car in cars]
disp = []
urls = [img[0] for img in imgs]
for url in urls:
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        original_image = Image.open(BytesIO(response.content)) 
        new_aspect_ratio = 5/3 
        original_aspect_ratio = original_image.width / original_image.height

        if original_aspect_ratio > new_aspect_ratio:
            new_width = original_image.width
            new_height = int(new_width / new_aspect_ratio)
        else:
            new_height = original_image.height
            new_width = int(new_height * new_aspect_ratio)

        new_image = Image.new("RGB", (new_width, new_height), (125, 125, 125))

        x_offset = (new_width - original_image.width) // 2
        y_offset = (new_height - original_image.height) // 2
        new_image.paste(original_image, (x_offset, y_offset))
        disp.append(new_image)

cols = [col1, col2, col3]
i = 0
for car in cars:
    button_key = f"button_{i}"
    carbrand = car.get("Brand").capitalize()
    carmodel = car.get("Model").capitalize()
    carmyear = car.get("Myear")
    carfuel = car.get("Fueltype").capitalize()
    cartransmission = car.get("Transmission").capitalize()
    carvariant = car.get("Variant").capitalize()
    carkms = car.get("Kms")
    carprice = car.get("Priceinlakh")
    a = cols[i % 3]
    with a:
        with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    border: 1px solid rgba(255, 255, 255, 1);
                    border-radius: 1rem;
                    padding: calc(0.75em - 1px)
                }
                """,
        ):
            col1, col2 = st.columns([0.999, 0.001])
            with col1:
                image = disp[i]
                st.image(disp[i], use_column_width = "always")
                st.markdown(f"#### {carmyear} {carbrand} {carmodel} {carvariant}")
                st.caption(f"{carfuel} · {cartransmission} · {int(car['Kms'] / 1e3)}k kms ")
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                st.markdown(f"### ₹{carprice} Lakh")
                st.write("")
            with col2:
                view = st.button(label = "View", key = button_key, use_container_width = True, type = "primary")
                i = i + 1
                if view:
                    st.session_state['car'] = car
                    switch_page('detailedlisting')
       
    


