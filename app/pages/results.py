import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import json
import utils
import numpy as np
from tensorflow.keras.saving import load_model


# hide side navbar
st.set_page_config(
    page_title = "Audio Similarity Service",
    initial_sidebar_state = "collapsed"
)

# additional styling
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {
                    display: none
        }
            
        [data-testid="stMetricValue"] {
            width: 100%;
            text-align: center;
            font-size: 50px;
            padding: 10% 0;
        }
            
        div[data-testid="column"]{
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# set session_state values
if 'song_upload' not in st.session_state:
    st.session_state.song_upload = None
if 'selected_song' not in st.session_state:
    st.session_state.selected_song = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'page_switch' not in st.session_state:
    st.session_state.page_switch = None

if st.session_state.page_switch:
    # perform here so page is not completely reloaded when switching pages
    switch_page("app")


# helper functions
def do_switch_page():
    st.session_state.selected_song = None
    st.session_state.song_upload = None
    st.session_state.results = None
    st.session_state.page_switch = True

@st.cache_data
def print_song(n, song):
    
        st.subheader(f"{n}) :violet[{song.track_title}]")

        col1, col2, col3 = st.columns([0.3,0.3,0.4])

        with col1:
            st.metric("Similarity", f"{float(song.vector_score):.2%}", delta=None, delta_color="normal", help="Cosine Similarity.", label_visibility="visible")

        with col2:
            st.subheader(":violet[Artist]")
            st.write(f"**{song.artist_name}**")
            st.subheader(":violet[Album]")
            st.write(f"**{song.album_title}**")

        with col3:
            st.write("")
            for attribute in [("Top Genre", song.genre_top),
                              ("Song Duration", song.duration),
                              ("Language", song.language_code),
                              ("Album Tracks", song.album_tracks)
                              ]:
                if attribute[1] != "null":
                    title, content = st.columns(2)
                    with title:
                            st.write(f"**:violet[{attribute[0]}]**")
                    with content:
                            st.write(attribute[1])


        spotify_id = utils.get_spotify_id(song.track_title, song.artist_name)
        if isinstance(spotify_id, str):
                st.components.v1.iframe(f"https://open.spotify.com/embed/track/{spotify_id}?utm_source=generator&theme=0", width=None, height=175, scrolling=False)
        elif isinstance(spotify_id, Exception):
            st.error(f"""
                       API Exception: {spotify_id}  
                       You are probably missing the client secret. Refer to the README.md
                       """, icon="⚠️")
        else:
            st.warning("Song not found on Spotify.", icon="⚠️")

        st.divider()


# main content
st.title("Audio Similarity Results")

# show uploaded song
if st.session_state.song_upload:
    # 🎼🎵🎶🎧🎹💾🔍📂▶️
    st.header("Your Song")
    st.subheader(f':violet[🎶 {st.session_state.song_upload.name}]')
    st.audio(st.session_state.song_upload, format="audio/wav", start_time=0, sample_rate=None)

    st.button("Back to Song Selection", use_container_width=True, on_click=do_switch_page)

    with st.spinner("Loading model..."):
        encoder = load_model("model/AEv3encoder3seconds")

    with st.spinner("Extracting features..."):
        feature_vector = utils.extract_features(st.session_state.song_upload, encoder)

    with st.spinner("Finding similar songs..."):
        st.session_state.results = utils.get_vector_similarity(feature_vector)


# show database selected song
elif st.session_state.selected_song:
    st.header("Your Song")
    song = st.session_state.df.loc[st.session_state.selected_song, :]
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader(":violet[Title]")
        st.write(f"**{song.track_title}**")

    with col2:
        st.subheader(":violet[Artist]")
        st.write(f"**{song.artist_name}**")

    with col3:
        st.subheader(":violet[Album]")
        st.write(f"**{song.album_title}**")

    spotify_id = utils.get_spotify_id(song.track_title, song.artist_name)
    if isinstance(spotify_id, str):
        st.components.v1.iframe(f"https://open.spotify.com/embed/track/{spotify_id}?utm_source=generator&theme=0", width=None, height=256, scrolling=False)
    elif isinstance(spotify_id, Exception):
        st.error(f"""
                    API Exception: {spotify_id}  
                    You are probably missing the client secret. Refer to the README.md
                    """, icon="⚠️")
    else:
        st.warning("Song not found on Spotify.", icon="⚠️")  

    st.button("Back to Song Selection", use_container_width=True, on_click=do_switch_page)

    with st.spinner("Extracting features..."):
        feature_vector_text = song["feature_vector_text"]
        feature_vector = np.array(json.loads(feature_vector_text))
    
    if st.session_state.results is None:
        print("Test")
        with st.spinner("Finding similar songs..."):
            st.session_state.results  = utils.get_vector_similarity(feature_vector, n_songs=51)

# show warning when no song selected (when manually navigating to /results)
else:
    st.warning("No song selected. Please go back and select a song to analyze.", icon="⚠️")
    st.button("Back to Song Selection", use_container_width=True, on_click=do_switch_page)


# showing results
if st.session_state.results is not None:

    st.header("Recommended Songs")

    n_results = st.slider("Number of results to display:", min_value=1, max_value=50, value=5, on_change=None, key="selector")

    progress_bar = st.progress(0, "Loading...")
    for idx, song in st.session_state.results.iloc[:n_results].iterrows():
        progress_bar.progress((idx/n_results), "Loading")
        print_song(idx+1, song)
    progress_bar.empty()

    st.button("Back to Song Selection", use_container_width=True, key="button-end", on_click=do_switch_page)