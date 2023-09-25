import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_extras.switch_page_button import switch_page
import pandas as pd

# Collapse sidebar on start
st.set_page_config(initial_sidebar_state="collapsed",layout="wide")

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
st.columns(3)[1].image("images/header.png",use_column_width="auto")

#"---"

col1, col2, col3, col4 = st.columns(4)

#    st.write("hhh")
df = pd.read_csv("pages/final_train.csv")
#st.dataframe(pd.DataFrame(df))
#st.write(df.km.min())
#st.write(df.km.max())
#st.write(sorted(df.km,reverse = True)[:10])

with col1:
    st.subheader("Filters")
    st.slider(label = "Price Range (in lacs)", min_value = round(df.listed_price.min() / 1000), max_value = round(df.listed_price.max() / 1000), value =  (4000,120000), step = 100)
    st.selectbox("Brand",df.oem.unique())
    st.radio("Fuel Type",df.fuel.unique())
    st.slider(label = "Year", min_value = df.myear.min(), max_value = df.myear.max(), value =  (2013,2019))
    st.radio("Transmission Type",df.transmission.unique())
   # st.radio("Kms Driven")
    #with st.expander("See explanation"):
    #    st.write("The chart above shows some numbers I picked for you I rolled actual dice for these so theyre guaranteed tobe random")

with col2:
    for i in range(0,2):
        with st.container():
            st.image("images/car_placeholder.png")
            st.write("This is inside the container")
            st.write("This is inside the container")
            st.write("This is inside the container")
        

with col3:
    for i in range(0,2):
        with st.container():
            st.image("images/car_placeholder.png")
            st.write("This is inside the container")
            st.write("This is inside the container")
            st.write("This is inside the container")
            

with col4:
    for i in range(0,2):
        with st.container():
            st.image("images/car_placeholder.png")
            st.write("This is inside the container")
            st.write("This is inside the container")
            st.write("This is inside the container")            
    
       
    


