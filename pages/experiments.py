import base64
from streamlit_extras.switch_page_button import switch_page
import streamlit as st
from st_clickable_images import clickable_images
import pymongo
from pymongo import MongoClient
car = st.session_state['car']
st.title(type(car))
st.write(car)
back = st.button("back")
if back:
    switch_page("listings")



