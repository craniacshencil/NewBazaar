import streamlit as st
from streamlit_extras.switch_page_button import switch_page
st.write(st.session_state['query'])
back = st.button("back")
if back:
    switch_page("listings")