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
st.session_state['image_list'] = []
image_list = []
# col1, col2 = st.columns([4, 1])
# with col1:
uploaded_images = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files = True)
# with col2:
#     st.button("Finish Upload")
#Accessing the images ===================gpt snippet===================
col1, col2, col3, col4= st.columns(4)
col_no = [col1, col2, col3, col4]
counter = 1
if uploaded_images:
    for uploaded_image in uploaded_images:
        image = Image.open(uploaded_image)
        st.write(image.width)
        st.write(image.height)
        image = image.resize((200, int(200 * image.height / image.width)))
        image_list.append(image)
        i = counter % 4 - 1
        a = col_no[i]
        with a:
            st.image(image, caption="Uploaded Image", use_column_width="never")
        counter = counter + 1

st.divider()
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    finish = st.button("Finish Upload")
if finish:
    st.session_state['image_list'] = image_list


        
