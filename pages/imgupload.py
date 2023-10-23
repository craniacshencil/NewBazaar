#Library imports
import streamlit as st
import time
from PIL import Image
import pillow_avif
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page
import os
import imgbbpy
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

#Checking login status
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

#Collapse and remove sidebar, add header image
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
st.columns(3)[1].image("images\\header.png", use_column_width="auto")

#Page title
colored_header(
label = "Upload Images: ",
description = " ",
color_name = "red-70",
)

#Creating session state to display images efficiently
st.session_state['img_list'] = []
if 'images_displayed' not in st.session_state:
    st.session_state['images_displayed'] = False
def set_images_displayed():
    st.session_state['images_displayed'] = True
# image_list = []

#URL generator function
image_urls = []
def urlgen(image_urls, img_path):
    client = imgbbpy.SyncClient('4ca08e789920c7f74605a4a461528c64')
    image = client.upload(file = img_path, expiration = 2592000)#Link valid for 30 days since creation
    image_urls.append(image.url)
    st.success("Process complete.")

#Creating uploader, displaying images and saving them locally.
uploaded_images = st.file_uploader("Upload images", type=["jpg", "jpeg", "png", "AVIF", "bmp", "webp"], accept_multiple_files = True)
st.info("Upload Landscape photos only")
display_button = st.columns(5)[2].button("Display Images", use_container_width = True, on_click = set_images_displayed)
col1, col2, col3, col4= st.columns(4)
col_no = [col1, col2, col3, col4]
counter = 1

if st.session_state['images_displayed']:
    for uploaded_image in uploaded_images:
        image = Image.open(uploaded_image)
        if image.mode in ("RGBA", "P"):#Converting photos with transparent backgrounds to jpg
            image = image.convert("RGB")
        disp_image = image.resize((200, int(200 * image.height / image.width)))
        imgpath = f"temp_storage\\image_{counter}.jpg"
        image.save(imgpath)
        i = counter % 4 - 1
        counter = counter + 1
        urlgen(image_urls, imgpath)
        with col_no[i]:
            st.image(disp_image, caption="Uploaded Image", use_column_width="never")
        

#Button for finishing upload
st.session_state['imageurls'] = []#initializing session state variable
st.divider()
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col3:    
    finish = st.button("Finish Upload", use_container_width = True)
with col4:
    back = st.button("Back", use_container_width = True)
if back:
    switch_page("displayval")
if finish:
    if st.session_state['images_displayed']:
        # st.session_state['images_displayed'] = None
        st.session_state['imageurls'] = image_urls
        switch_page("listingpreview")
    else:
        st.error("Confirm the Images first")

        
