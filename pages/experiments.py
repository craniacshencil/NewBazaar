import streamlit as st
from streamlit_extras.grid import grid 
import pandas as pd
import numpy as np
import plotly.express as px

labels = ['Down Payment', 'Principal Loan Amount', 'Interest Payable']
selected_value = st.slider('Select a value:', min_value=0, max_value=100, value=50)
values = [selected_value, 100 - selected_value, 0, 0]
fig = px.pie(names=labels, values=values, hole=0.4, title='Dynamic Doughnut Chart')
st.plotly_chart(fig)








