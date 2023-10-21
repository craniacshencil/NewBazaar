#library imports
import streamlit as st
import numpy as np
import time
from PIL import Image
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page
from streamlit_carousel import carousel
import glob
import os
import shutil

#Empty out the entire folder
for filename in os.listdir("temp_storage"):
    filepath = os.path.join("temp_storage", filename)
    try:
        shutil.rmtree(filepath)
    except OSError:
        os.remove(filepath)

#Webpage settings and header config
st.set_page_config(initial_sidebar_state = "collapsed", layout = "wide")
image = Image.open("images\\header.png")
image = image.resize((300, int(300 * image.height / image.width)))
st.columns(3)[1].image(image)
colored_header(
label = "Confirm Listing: ",
description = " ",
color_name = "red-70",
)

#Generating carousel out of urls
col1, col2 = st.columns([8, 5])
with col1:
    image_urls = st.session_state['imageurls']
    img_collection = []
    for url in image_urls:
        item = dict(title = "",
                    text = "",
                    interval = None,
                    img = url)
        img_collection.append(item)
        carousel(items = img_collection, width = 1)

#Converting values back
values = st.session_state['values']
if values[5] == 0:
        values[5] = "Manual"
else:
        values[5] = "Automatic"

if values[4] == 0:
        values[4] = "LPG"
if values[4] == 1:
        values[4] = "CNG"
if values[4] == 2:
        values[4] = "Petrol"
if values[4] == 3:
        values[4] = "Diesel"
if values[4] == 4:
        values[4] = "Electric"

if values[6] == 1:
      values[6] = "1st"
if values[6] == 2:
      values[6] = "2nd"
if values[6] == 3:
      values[6] = "3rd"
if values[6] == 4:
      values[6] = "4th"
if values[6] == 5:
      values[6] = "5th"
else:
      values[6] = "6th"

#Adding important text

with col2:
    st.markdown(f"# {values[1]} {values[0].capitalize()} {values[2].capitalize()}")
    st.markdown(f"## {values[3]} · {values[4]} · {values[5]}")
    st.markdown(f"## {values[6]} owner · {values[7]} kms")

st.write("yay! a Carousel")
#  values = [brand, yr, model, variant, fueltype
#          , transmission, owner, kms]