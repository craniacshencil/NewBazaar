import streamlit as st
from streamlit_extras.switch_page_button import switch_page
names = ['one', 'two']
checkboxes = []
for i, name in enumerate(names):
    key = f"checkbox_{i}"
    checkbox = st.checkbox(label = name, key = key)
    checkboxes.append(checkbox)

selected = []
confirm = st.button("confirm")
if confirm:
    for box in checkboxes:
        selected.append(box)
    true_vals = [name for name in names if checkboxes[names.index(name)] == True]
    st.write(true_vals)

back = st.columns(2)[1].button("back", use_container_width= True)
if back:
    switch_page('dashboard')
