import base64
import streamlit as st
from st_clickable_images import clickable_images

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
st.title("making sure the screen is not limited to the center and that there is space on either sides")
images = []
for file in ["images//buy_now.png", "images//sell_ride.png"]:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/jpeg;base64,{encoded}")

clicked = clickable_images(
    images,
    titles=[f"Image #{str(i)}" for i in range(2)],
    div_style={"display": "block", "justify-content": "flex-start", "flex-wrap": "nowrap", "width" : "1100px"},
    img_style={"margin": "1px", "height": "500px", "width" : "500px"},
)

st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")








