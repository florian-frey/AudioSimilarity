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

st.write('You selected track_id', st.session_state.track_id)

st.dataframe(st.session_state.df.loc[st.session_state.track_id, :])

if st.button("Home"):
    switch_page("app")