import streamlit as st
import numpy as np
import librosa
import matplotlib.pyplot as plt
from api_functions import *
from st_pages import Page, show_pages, add_page_title, hide_pages
import webbrowser
from streamlit_extras.switch_page_button import switch_page
from feature_extraction import *

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

# show_pages(
#     [
#         Page("app.py", "Home", "🏠"),
#         Page("pages/song2.py", "Song 2", "🎵"),
#         Page("pages/results.py", "Results", "📊")
#     ]
# )


st.title("Audio Similarity")


# search for song via spotify api
if 'song1_id' not in st.session_state:
    st.session_state.song1_id = None

def search():
    song_id = get_song_id(title, artist)
    if song_id:
        st.session_state.song1_id = song_id
    else:
        st.warning(' No Track found.', icon="⚠️")

st.header("Spotify API")
title = st.text_input("Song 1", label_visibility="collapsed", placeholder="title", key="search1title")
artist = st.text_input("Song 1", label_visibility="collapsed", placeholder="artist", key="search1artist")

st.button("Search", on_click=search)

st.write("ID:", st.session_state.song1_id)

st.components.v1.iframe(f"https://open.spotify.com/embed/track/{st.session_state.song1_id}?utm_source=generator&theme=0", width=None, height=352, scrolling=False)

if st.button("Kowalski, Analysis!"):
    switch_page("results")


# upload own audio file
st.header("File Upload")
audio = st.file_uploader("Upload song", type=["mp3", "wav"], accept_multiple_files=False,
                         key=None, help="Tooltip", on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

if audio is not None:
    st.write(audio)
    st.audio(audio, format="audio/wav", start_time=0, sample_rate=None)

    with st.spinner(text="Extracting features..."):
        features = extract_features(audio)
        st.write(features)


# database search
st.header("Database Search")

find = st.button("Query Database")

if find:
    with st.spinner(text="Querying database..."):
        conn = st.experimental_connection("sql", type=None, max_entries=None, ttl=None, url=f"postgresql://postgres:{st.secrets['sql']['password']}@localhost:5432/fma")
        # df = conn.query("SELECT * FROM tracks LIMIT 10;")
        songs = conn.query("SELECT track_title FROM tracks ORDER BY track_title;")
        # st.dataframe(df)

        option = st.selectbox("Find song", songs)

        st.write('You selected:', option)
