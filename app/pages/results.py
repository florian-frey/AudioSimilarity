import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import utils
import numpy as np

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
            font-size: 75px;
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
if 'page' not in st.session_state:
    st.session_state.page = 0


# helper functions
@st.cache_data
def print_song(n, song):
    
        st.subheader(f"{n}) :violet[{song.track_title}]")

        col1, col2, col3 = st.columns([0.3,0.3,0.4])

        with col1:
            st.metric("Similarity", "92%", delta=None, delta_color="normal", help="Cosine Similarity.", label_visibility="visible")

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
                st.components.v1.iframe(f"https://open.spotify.com/embed/track/{spotify_id}?utm_source=generator&theme=0", width=None, height=256, scrolling=False)
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



st.header("Your Song")


if st.session_state.song_upload:
    # 🎼🎵🎶🎧🎹💾🔍📂▶️
    st.subheader(f'🎶 {st.session_state.song_upload.name}')
    st.audio(st.session_state.song_upload, format="audio/wav", start_time=0, sample_rate=None)

    with st.spinner("Finding similar songs..."):
        vec = np.random.rand(100)
        results = utils.get_vector_similarity(vec)

elif st.session_state.selected_song:
    song = st.session_state.df.loc[st.session_state.selected_song, :]

    # st.write('You selected song', st.session_state.selected_song)
    # st.subheader(f":violet[{song.track_title}]")

    col1, col2, col3 = st.columns(3)

    with col1:
        # st.markdown("# :headphones:")
        st.subheader(":violet[Title]")
        st.write(f"**{song.track_title}**")

    with col2:
        st.subheader(":violet[Artist]")
        st.write(f"**{song.artist_name}**")

    with col3:
        st.subheader(":violet[Album]")
        st.write(f"**{song.album_title}**")

    spotify_id = utils.get_spotify_id(song.track_title, song.artist_name)
    if spotify_id:
        st.components.v1.iframe(f"https://open.spotify.com/embed/track/{spotify_id}?utm_source=generator&theme=0", width=None, height=256, scrolling=False)
    else:
        st.warning("Song not found on Spotify.", icon="⚠️")    

    # st.dataframe(song)

    # string = song["feature_vector"]
    # bytestring = bytes(string)

    # st.write(string)
    # st.write(bytestring)
    

    # with st.spinner("Finding similar songs..."):
        # utils.get_vector_similarity(song["feature_vector"])

    with st.spinner("Finding similar songs..."):
        vec = np.random.rand(100)
        results = utils.get_vector_similarity(vec)

else:
    st.warning("No song selected. Please go back and select a song to analyze.")
    if st.button("Home", key="button-nosong"):
        switch_page("app")


if st.button("Back to Song Selection", use_container_width=True):
    st.session_state.selected_song = None
    st.session_state.song_upload = None
    switch_page("app")


# results
st.header("Recommended Songs")


n_results = st.slider("Number of results to display:", min_value=1, max_value=50, value=5, on_change=None, key="selector")

# results_container = st.container()

results = utils.get_vector_similarity(vec, n_songs=n_results)
for n, (idx, song) in enumerate(results.iterrows()):
    print_song(n+1, song)
    # st.divider()
        
# def load_songs():
#     st.session_state.page +=1
#     more_results = utils.get_vector_similarity(vec, page=st.session_state.page)
#     for n, (idx, song) in enumerate(more_results.iterrows()):
#         print_song(n+1+5*st.session_state.page, song)
#         # st.divider()

# st.button("Load more", on_click=load_songs, use_container_width=True)

if st.button("Back to Song Selection", use_container_width=True, key="button-end"):
    st.session_state.selected_song = None
    st.session_state.song_upload = None
    switch_page("app")