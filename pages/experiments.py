import base64
import streamlit as st
from st_clickable_images import clickable_images
import pymongo
from pymongo import MongoClient
car = st.session_state['car']
st.title(type(car))
st.write(car)




