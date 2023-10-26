import pandas as pd
import streamlit as st
df = pd.read_csv("data//pred_data.csv")
df2 = pd.read_csv("data//train3.csv")
st.write(df2)
st.write(df)
st.write(df.shape)
idx = len(df)
st.write(idx)
df.loc[idx, "myear"] = 2019
st.write(df.tail(3))