import streamlit as st
import pandas as pd
import time
import pickle
from streamlit_extras.colored_header import colored_header
from streamlit_extras.switch_page_button import switch_page


df = pd.read_csv("data/train3.csv")
df2 = pd.read_csv("data/data_entry_train.csv")

#def main():
#Loading the model
st.set_page_config(initial_sidebar_state = "collapsed", layout = "wide")
pickle_in = open('models\predictor.pkl', 'rb')
cat_model = pickle.load(pickle_in)
st.columns(3)[1].image("images\header.png",use_column_width="auto")
#st.subheader('About your car: ')
colored_header(
label = "About your Car: ",
description = "Enter the mentioned details",
color_name = "red-70",
)
#st.divider()
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
        brand = st.selectbox("Enter the brand of your car: "
                        , df['oem'].unique())
        #st.divider()
        yr = st.selectbox("Enter registration year of car: "
                        , sorted(df.loc[df.oem == brand]['myear'].unique()
                                , reverse = True))
        #st.divider()
        model = st.selectbox("Enter the model of your car: "
                        , df.loc[(df.oem == brand)
                                & (df.myear == yr)]['model'].unique())
        #st.divider()
        variant = st.selectbox("Enter the variant: "
                        , df.loc[(df.model == model)
                                & (df.myear == yr)]['variant'].unique())
        #st.divider()
        fueltype = st.selectbox("Enter fuel: ",
                                df2.loc[(df2.model == model)
                                & (df2.myear == yr)
                                & (df2.variant == variant)]['fuel'].unique())
        
        #st.divider()
        transmission = st.selectbox('Enter transmission: ',
                                df2.loc[(df2.myear == yr) & 
                                        (df2.model == model) &
                                        (df2.variant == variant) &
                                        (df2.fuel == fueltype)]['transmission'].unique())

        owner = st.selectbox("Enter owner-number: ", 
                        df['owner_type'].unique())
        st.info("here 1 = first owner")
        #st.divider()
        kms = st.number_input("Enter kms driven: ", min_value = 0
                        , max_value = 130000, step = 5000)

st.session_state['kms'] = 'not set'
if kms != 0:
        st.session_state['kms'] = 'set'
st.divider()
if transmission == 'manual':
        transmission = 0
else:
        transmission = 1

if fueltype == 'lpg':
        fueltype = 0
if fueltype == 'cng':
        fueltype = 1
if fueltype == 'petrol':
        fueltype = 2
if fueltype == 'diesel':
        fueltype = 3
if fueltype == 'electric':
        fueltype = 4
#st.divider()
confirmation = st.columns(7)[3].button("Confirm details")
if(confirmation):
        if st.session_state['kms'] == 'not set':
                st.error("You have not entered kms driven.")
        if(st.session_state['kms'] == 'set'):  
                progress_text = "Saving Details..."
                my_bar = st.progress(0, text = progress_text)

                for percent_complete in range(100):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1, text=progress_text)
                
                values = [brand, yr, model, variant, fueltype
                        , transmission, owner, kms]
                temp = df.loc[(df.oem == values[0]) 
                & (df.myear == values[1]) 
                & (df.model == values[2]) 
                #& (df.variant == values[3])
                & (df.fuel == values[4])
               ]
                tc = temp['Turbo Charger'].mode()[0]
                kw = temp['Kerb Weight'].mean()
                dt = temp['Drive Type'].mode()[0]
                seats = temp['Seats'].mode()[0]
                tspeed = temp['Top Speed'].mean()
                acc = temp['Acceleration'].mean()
                doors = temp['Doors'].mode()[0]
                cvolume = temp['Cargo Volume'].mean()
                maxTorque = temp['Max Torque Delivered'].mean()
                measure = temp['avg_measure'].mean()
                feat = temp['Features'].mode()[0]
                valves = temp['Valves'].mode()[0]
                tread = temp['Tread'].mean()
                
                #predictors = [myear, transmission, fuel, km, Turbo Charger, kerb weight, drive type
                # ,seats, top speed, Acceleration, Doors, Cargo Volume, owner_type,
                # Max Torque Delivered, avg_measure, Features, valves, tread]
                predictors = [values[1], values[5], values[4], values[7], 
                                tc, kw, dt, seats, tspeed, acc, doors, cvolume,
                                values[6], maxTorque, measure, feat, valves, tread]
                
                pred = cat_model.predict(predictors)
                st.session_state['pred'] = pred
                st.session_state['values'] = values
                #pred = predict_price(values, cat_model)
                time.sleep(1)       
                st.success("Details have been registered.")

                with st.spinner("Calculating price..."):
                        time.sleep(2)
                switch_page("displayval")

                '''if pred >= 1e7:
                        pred = pred / 1e7
                        colored_header(label = f"The predicted price is: ₹{round(pred, 2)} Cr",
                                description = " ",
                                color_name = 'red-70')
                elif (pred > 1e5):
                        pred = pred / 1e5 
                        colored_header(label = f"The predicted price is: ₹{round(pred, 2)} Lakh",
                                        description = " ",
                                        color_name = 'red-70')'''