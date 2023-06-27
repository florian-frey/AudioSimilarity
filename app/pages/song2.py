import streamlit as st

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


st.title("Audio Similarity")

if 'song2_id' not in st.session_state:
    st.session_state.song2_id = None

def search():
    song_id = get_song_id(title, artist)
    st.session_state.song2_id = song_id

st.header("Song 2")
title = st.text_input("Song 2", label_visibility="collapsed", placeholder="title", key="search1title")
artist = st.text_input("Song 2", label_visibility="collapsed", placeholder="artist", key="search1artist")

st.button("Search", on_click=search)

st.write("ID:", st.session_state.song2_id)

st.components.v1.iframe(f"https://open.spotify.com/embed/track/{st.session_state.song2_id}?utm_source=generator&theme=0", width=None, height=352, scrolling=False)
