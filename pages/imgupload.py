#Library imports
import streamlit as st
import time
from PIL import Image
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page
import os
import imgbbpy


#Page Config and Header
st.set_page_config(initial_sidebar_state = "collapsed", layout = "wide")
st.columns(3)[1].image("images\\header.png", use_column_width="auto")
colored_header(
label = "Upload Images: ",
description = " ",
color_name = "red-70",
)
# st.session_state['image_list'] = []
# image_list = []

#URL generator function
image_urls = []
def urlgen(image_urls, img_path):
    client = imgbbpy.SyncClient('4ca08e789920c7f74605a4a461528c64')
    image = client.upload(file = img_path, expiration = 300)
    image_urls.append(image.url)
    st.success("Process complete.")

#Creating uploader, displaying images and saving them locally.
uploaded_images = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files = True)
st.info("Upload Landscape photos only")
col1, col2, col3, col4= st.columns(4)
col_no = [col1, col2, col3, col4]
counter = 1
if uploaded_images:
    for uploaded_image in uploaded_images:
        image = Image.open(uploaded_image)
        #image.convert("RGB")#convert to jpg format
        if image.mode in ("RGBA", "P"):#Converting photos with transparent backgrounds to jpg
            image = image.convert("RGB")
        disp_image = image.resize((200, int(200 * image.height / image.width)))
        if image.height > image.width:
            image = image.resize((int(image.width / 4), int(image.height / 4)))
            image = image.crop()
        imgpath = f"temp_storage\\image_{counter}.jpg"
        image.save(imgpath)

        i = counter % 4 - 1
        a = col_no[i]
        urlgen(image_urls, imgpath)
        with a:
            st.image(disp_image, caption="Uploaded Image", use_column_width="never")
        counter = counter + 1

#Generating urls for each image


#Button for finishing upload
st.session_state['imageurls'] = []#initializing session state variable
st.divider()
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    finish = st.button("Finish Upload")
if finish:
    st.session_state['imageurls'] = image_urls
    switch_page("listingpreview")



        
