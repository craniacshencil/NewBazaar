import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
import pandas as pd

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

authentication_status = st.session_state["authentication_status"]

st.columns(3)[1].image("images/header.png",use_column_width="auto")

if not authentication_status:
    authenticator.logout('Logout', 'main')
    # st.write(f'Welcome *{name}*')
    #switch_page("login")

# Connect to Deta Base
#deta = Deta(st.secrets["data_key"])
#db = deta.Base("car_bazaar")

df = pd.read_csv("pages/final_train.csv")
brand = st.selectbox("Brand",df.oem.unique())
model = st.selectbox("Model",df.loc[df.oem == brand]["model"].unique())
variant = st.selectbox("Varient",df.loc[df.model == model]["variant"].unique())

st.dataframe(df)

with st.form("form"):
    brand = st.selectbox("Brand",df.oem.unique())
    model = st.selectbox("Model",df.loc[df.oem == brand]["model"].unique())
    variant = st.selectbox("Model",df.loc[df.model == model]["variant"].unique())
    fuel = st.selectbox("Fuel Type",df.fuel.unique())
    myear = st.slider(label = "Manufacturing Year", min_value = df.myear.min(), max_value = df.myear.max())
    transmission = st.radio("Transmission Type",df.transmission.unique())
    uploaded_file = st.file_uploader("Upload images", accept_multiple_files = True)
    #name = st.text_input("Your name")
    #age = st.number_input("Your age")
    submitted = st.form_submit_button("Store in database")

# If the user clicked the submit button,
# write the data from the form to the database.
# You can store any data you want here. Just modify that dictionary below (the entries between the {}).
#if submitted:
#    db.put({"brand": brand, 
#            "fuel": fuel,
#            "myear": myear
#            })

"---"
"Here's everything stored in the database:"



# This reads all items from the database and displays them to your app.
# db_content is a list of dictionaries. You can do everything you want with it.

#db_content = db.fetch().items
#st.write(db_content)




