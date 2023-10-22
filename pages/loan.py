import streamlit as st
from streamlit_extras.colored_header import colored_header
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state = "collapsed", layout = "wide")
st.columns(3)[1].image("images\\header.png", use_column_width="auto")
colored_header(
label = "Loan Calculator: ",
description = " ",
color_name = "red-70",
)
price = st.session_state['Price']
full_price = price * 1e5
values = st.session_state['values']
def loan_amount(p,r,t):
    r = r / 1200
    m = t*12
    emi = (p*r*(1+r)**m) / ((1+r)**m-1)
    payable_interest = (emi*m) - p
    total_amount = emi*m 
    return emi, payable_interest, total_amount

st.markdown(f"## {values[1]} {values[0].capitalize()} {values[2].capitalize()} {values[3]} - ₹{price} Lakh")
st.divider()
col1, col2, col3 = st.columns([0.35, 0.4, 0.25])
with col1:
    st.subheader("")
    st.subheader("")
    st.write("")
    full_price = price * 1e5
    principal_in_lakhs = st.slider('Principal amount (in lakhs)',min_value=1.0, max_value= price, step = 0.1)
    principal = principal_in_lakhs * 100000 
    interest_rate = st.slider('Interest rate', min_value=5.0, max_value=20.0, step = 0.5)
    term = st.slider('Term (in years)', min_value=1, max_value=20, step = 1)
    margin, col1 = st.columns([2, 3])
    
emi , payable_interest, total_amount = loan_amount(principal, interest_rate, term)

with col2:
    labels = ['Down Payment', 'Principal Loan Amount', 'Interest Payable']
    label_val = [full_price - principal, principal, payable_interest]
    colors = ["#c48c12", "#ba3a3a", "#d45004"]
    fig = go.Figure(data = [go.Pie(labels = labels, values = label_val, hole = 0.5)])
    # fig = px.pie(names = labels, values = label_val, hole = 0.5, title = 'Finance Breakdown')
    fig.update_traces(marker=dict(colors=colors))
    fig.update_layout(legend=dict(x = 0, y = 1))
    st.plotly_chart(fig)

with col3:
    st.title("")
    st.title("")
    st.title("")
    st.title("")
    if emi > 1e5:
        st.markdown(f"#### EMI : ₹{emi / 1e5:.2f} Lakh")
    else:
        st.markdown(f"#### EMI : ₹{emi / 1e3:.2f} Thousand")
    if total_amount > 1e7:
        st.markdown(f"#### Total amount: ₹{total_amount / 1e7:.2f} Cr")
    else:
        st.markdown(f"#### Total amount: ₹{total_amount / 1e5:.2f} Lakh")
    st.write("")
    if payable_interest > 1e5:
        st.markdown(f"##### Payable Interest: ₹{payable_interest / 1e5:.2f} Lakh")
    else:
        st.markdown(f"##### Payable Interest: ₹{payable_interest / 1e3:.2f} Thousand")
st.divider()
back = st.columns(7)[3].button("Return to listing")
if back:
    switch_page("listingpreview")