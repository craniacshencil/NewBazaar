import streamlit as st
from streamlit_extras.switch_page_button import switch_page
back = st.columns(2)[1].button("back", use_container_width= True)
if back:
    switch_page('listings')