#library imports
import streamlit as st
import numpy as np
import pandas as pd
import time
from PIL import Image
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_carousel import carousel
from streamlit_extras.stylable_container import stylable_container 
from streamlit_extras.grid import grid
import pymongo
from pymongo import MongoClient
import glob
import os
import shutil
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


#Collapsing and removing sidebar, adding header image
st.set_page_config(initial_sidebar_state = "collapsed", layout = "wide")
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

image = Image.open("images\\header.png")
image = image.resize((300, int(300 * image.height / image.width)))
st.columns(3)[1].image(image)
colored_header(
label = "Confirm Listing: ",
description = " ",
color_name = "red-70",
)

#Bringing in the required car
car = st.session_state['car']

#Generating carousel out of urls
col1, col2 = st.columns([2, 1], gap = "small")
with col1:
    image_urls = car['Images']
    img_collection = []
    for url in image_urls:
        item = dict(title = "",
                    text = "",
                    interval = None,
                    img = url)
        img_collection.append(item)
    carousel(items = img_collection, width = 1)

#Car Overview
with col2:
    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 2px solid rgba(60, 60, 60, 1);
                border-radius: 1rem;
                padding: calc(1em - 1px)
            }
            """,
    ):

        st.markdown(f"##### {car['Myear']} {car['Brand'].capitalize()} {car['Model'].capitalize()} {car['Variant'].capitalize()}")
        st.markdown(f"###### {int(car['Kms'] / 1e3)}k kms · {car['Fueltype'].capitalize()} · {car['Transmission'][5]} · {car['Ownerno']} owner ")
        col1, col2, col3 = st.columns([1, 40, 1])
        with col2:
            st.divider()
        col1, col2 = st.columns([1, 3])
        with col2:
            st.markdown(f"####  Price: ₹{price} Lakh")
            # st.caption("(Fixed On-road price)")
        col1, col2, col3 = st.columns([1, 40, 1])
        with col2:
            st.divider()
        col0, col1, col2 = st.columns(3)
        with col0:
            wishlist = st.button("Wishlist", use_container_width = True)
        with col2:
            emi = st.button("Calculate EMI", use_container_width = True)
        with col1:
            st.link_button("Contact Seller on Whatsapp", f"https://wa.me/{phonenumber}", type = "primary", use_container_width = True)
if(wishlist):
	st.toast("Added to wishlist")
if(emi):
    switch_page("loan")
#  values = [brand, yr, model, variant, fueltype
#          , transmission, owner, kms]

#Displaying Basic details of the car
df = pd.read_csv("data\\data_entry_train.csv")
df = df.loc[(df.model == values[2]) & (df.variant == values[3])]

valve_config = df['Valve Configuration'].mode()[0]
kerb_wt = df['Kerb Weight'].mode()[0]
seats = df['Seats'].mode()[0]
max_torque = df['Max Torque Delivered'].mode()[0]
body = df['body'].mode()[0]
gearbox = df['Gear Box'].mode()[0]
steering_type = df['Steering Type'].mode()[0]
F_brake = df['Front Brake Type'].mode()[0]
R_brake = df['Rear Brake Type'].mode()[0]
tyres = df['Tyre Type'].mode()[0]
Fuelsupplysystem = df['Fuel Supply System'].mode()[0]
tread = df['Tread'].mode()[0]

st.divider()
with stylable_container(
    key="container_with_border",
    css_styles="""
        {
            border: 2px solid rgba(60, 60, 60, 1);
            border-radius: 1rem;
            padding: calc(1em - 1px)
        }
        """,
):
    st.subheader("General Features")
    my_grid = grid(4, vertical_align="bottom")
    # Row 1:
    my_grid.text_input(label = "Body", value = body.capitalize(), disabled = True)
    my_grid.text_input(label = "GearBox", value = gearbox, disabled = True)
    my_grid.text_input(label = "Seats", value = seats, disabled = True)
    my_grid.text_input(label = "Max Torque", value = f"{int(max_torque)} Nm", disabled = True)
    # Row 2:
    my_grid.text_input(label = "Fuel-Supply System", value = Fuelsupplysystem, disabled = True)
    my_grid.text_input(label = "Tyres", value = tyres.capitalize(), disabled = True)
    my_grid.text_input(label = "Steering Type", value = steering_type.capitalize(), disabled = True)
    my_grid.text_input(label = "Front Brake", value = F_brake.capitalize(), disabled = True)
    # Row 3:
    my_grid.text_input(label = "Rear Brake", value = R_brake.capitalize(), disabled = True)
    my_grid.text_input(label = "Tread", value = f"{str(int(tread))}", disabled = True)
    my_grid.text_input(label = "Valve Configuration", value = valve_config, disabled = True)
    my_grid.text_input(label = "Kerb Weight", value = f"{str(int(kerb_wt))}", disabled = True)

#Go Back to Dashboard and adding the listing to Database
finish = st.columns(5)[2].button("Confirm listing")
if(finish):
    client = MongoClient("localhost", 27017)
    db = client.carbazaar
    listing = db.listings

    #  values = [brand, yr, model, variant, fueltype
    #          , transmission, owner, kms]
    post = {
        "Seller" : name,
        "Phonenumber" : phonenumber,
        "Priceinlakh" : price,
        "Images" : image_urls,
        "Brand" : values[0], 
        "Myear" : int(values[1]), 
        "Model" : values[2],
        "Variant" : values[3],
        "Fueltype" : values[4],
        "Transmission" : values[5],
        "Ownerno" : values[6],
        "Kms" : values[7],
        "Valveconfiguration" : valve_config,
        "Kerbweight" : int(kerb_wt),
        "Seats" : int(seats),
        "Maxtorque" : int(max_torque),
        "Body" : body,
        "Gearbox" : gearbox,
        "Steeringtype" : steering_type,
        "Frontbrake" : F_brake,
        "Rearbrake" : R_brake,
        "Tyres" : tyres,
        "Fuelsupplysystem" : Fuelsupplysystem,
        "Tread" : int(tread)
    }

    listings = db.post
    listings.insert_one(post).inserted_id
    st.success("Your Car has been successfully listed")
    st.toast("Redirecting to dashboard in 3 sec..")
    time.sleep(3)
    switch_page("dashboard")