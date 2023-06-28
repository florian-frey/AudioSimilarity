import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# hide side navbar
st.set_page_config(
    initial_sidebar_state="collapsed"
)
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Audio Similarity Results")

if st.button("Home"):
    switch_page("app")