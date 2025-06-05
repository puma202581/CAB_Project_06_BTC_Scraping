# To install Streamlit, run the following command in your terminal:
# pip install streamlit

import streamlit as st

st.title("Hello World")

favourite_mentor = st.selectbox(
    "Who is your favourite CAB mentor?",
    ("Emily", "Muayad", "Raul", "Lucas", "Janina"),
    index=None,
    placeholder="Select your favourite mentor"
)

st.write("Your favourite mentor is: ", favourite_mentor)
