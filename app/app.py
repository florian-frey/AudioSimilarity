import streamlit as st
# import spotify_api
# from st_pages import Page, show_pages, add_page_title, hide_pages
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
# if 'song1_id' not in st.session_state:
#     st.session_state.song1_id = None

# def search():
#     song_id = spotify_api.get_song_id(title, artist)
#     if song_id:
#         st.session_state.song1_id = song_id
#     else:
#         st.warning(' No Track found.', icon="⚠️")

# st.header("Spotify API")
# title = st.text_input("Song 1", label_visibility="collapsed", placeholder="title", key="search1title")
# artist = st.text_input("Song 1", label_visibility="collapsed", placeholder="artist", key="search1artist")

# st.button("Search", on_click=search)

# st.write("ID:", st.session_state.song1_id)

# st.components.v1.iframe(f"https://open.spotify.com/embed/track/{st.session_state.song1_id}?utm_source=generator&theme=0", width=None, height=352, scrolling=False)

# if st.button("Kowalski, Analysis!"):
#     switch_page("results")



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

def song_title(id):
    try:
        return f"{st.session_state.df.loc[id, 'track_title']} [{st.session_state.df.loc[id, 'artist_name']}]"
    except:
        return id

if 'query_db' not in st.session_state:
    st.session_state.query_db = None
    st.session_state.df = None

if not st.session_state.query_db:
    if st.button("Query Database"):
        with st.spinner(text="Querying database..."):
            conn = st.experimental_connection("postgres", type="sql")
            st.session_state.df = conn.query("SELECT track_id, track_title, album_title, album_date_released, artist_name FROM tracks ORDER BY track_title;")
            st.session_state.df.index = st.session_state.df["track_id"]

        st.session_state.query_db = True
        st.experimental_rerun()
            
else:
    st.dataframe(st.session_state.df)

    option = st.selectbox("Search for song in database", ["<select>"]+list(st.session_state.df["track_id"]), format_func=song_title)

    if option != "<select>":
        st.write('You selected track_id', option)
        if st.button("Show results."):
            switch_page("results")