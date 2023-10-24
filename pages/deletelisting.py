import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_extras.switch_page_button import switch_page
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
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

# Remove sidebar via CSS and adding header image
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
st.columns(3)[1].image("images\\header.png" ,use_column_width="auto")
st.header("Delete listing", divider = "red")

#MongoDB config and bringing in the car to be deleted
client = MongoClient("localhost", 27017)
db = client.carbazaar
cars = db.post
car = st.session_state['deletedcar']
#content
finalsold = st.number_input(f"Enter the final selling price of your {car['Myear']} {car['Brand']} {car['Model']} {car['Variant']}",
                            value = None, placeholder = "Enter price in Lakh")
st.info("This is a compulsory field")
dummy = st.columns(7)[3].button(label = "Confirm Price", use_container_width = True)
if dummy:
    if finalsold != None:
        #Finding and deleting the car
        cars.delete_one({'_id' : ObjectId(car['_id'])})
        st.success("Listing deleted")
        st.success("Thank You for using CarBazaar")
        st.toast("Redirecting to mylistings")
        switch_page("mylisting.py")
    else:
        st.error("Enter a price")
        