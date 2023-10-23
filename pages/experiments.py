import base64
import streamlit as st
from st_clickable_images import clickable_images
import pymongo
from pymongo import MongoClient
#MongoDB config
client = MongoClient("localhost", 27017)
db = client.carbazaar
listings = db.post
cars = listings.find()

myear = [car.get('Myear') for car in cars]
price = [car.get('Priceinlakh') for car in cars]
brand = [car.get('Brand') for car in cars]
model = [car.get('Model') for car in cars]
variant = [car.get('Variant') for car in cars]
fuel = [car.get('Fueltype') for car in cars]
kms = [car.get('Kms') for car in cars]
transmission = [car.get('Transmission') for car in cars]

atts = [price, myear, brand, model, variant, fuel, kms, transmission]
lens = [len(att) for att in atts]
for car in cars:
    st.write(car)




