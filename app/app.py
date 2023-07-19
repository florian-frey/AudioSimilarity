import streamlit as st
# import spotify_api
# from st_pages import Page, show_pages, add_page_title, hide_pages
from streamlit_extras.switch_page_button import switch_page
from feature_extraction import *
from redis import Redis
from redis.commands.search.query import Query

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



# redis database search

redis_conn = Redis(host='localhost', port=6379, password=None)

st.header("Redis Database Search")

def base_query(return_fields: list=[], number_of_results: int=20):
    base_query = f'*'
    query = Query(base_query)\
        .paging(0, number_of_results)\
        .dialect(2)
    
    results = redis_conn.ft("audiosimilarity").search(query)

    if results.docs:
        return pd.DataFrame(list(map(lambda x: {'id': x.id, 'track_title' : x.track_title, 'album_title': x.album_title, 'artist_name': x.artist_name}, results.docs))).sort_values(by='id')
    else:
        return pd.DataFrame()

def get_song_info(id):
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
            st.session_state.df = base_query(number_of_results=10000)
            st.session_state.df["track_id"] = st.session_state.df["id"].str[16:]
            st.session_state.df.index = st.session_state.df["track_id"]
            st.session_state.query_db = True
            st.experimental_rerun()
            
else:
    # st.dataframe(st.session_state.df)
    st.write(str(len(st.session_state.df)), "songs found.")

    if 'track_id' not in st.session_state:
        st.session_state.track_id = None

    with st.spinner("Loading Song..."):
        st.session_state.track_id = st.selectbox("Search for song in database", [""]+list(st.session_state.df["track_id"]), format_func=get_song_info)


    if st.session_state.track_id:
        if st.button("Show results."):
            with st.spinner("Loading..."):
                switch_page("results")





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


# st.audio("https://storage.googleapis.com/kagglesdsdata/datasets/1130776/1897587/fma_medium/fma_medium/004/004027.mp3")