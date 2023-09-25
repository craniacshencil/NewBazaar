import streamlit as st
import time
from PIL import Image
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page
st.set_page_config(initial_sidebar_state = "collapsed", layout = "wide")
st.columns(3)[1].image("images\header.png", use_column_width="auto")
colored_header(
label = "Upload Images: ",
description = " ",
color_name = "red-70",
)
uploaded_images = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files = True)




#Accessing the images ===================gpt snippet===================
#if uploaded_images:
    #for uploaded_image in uploaded_images:
        # Display each uploaded image
        #image = Image.open(uploaded_image)
        #st.image(image, caption="Uploaded Image", use_column_width=True)
