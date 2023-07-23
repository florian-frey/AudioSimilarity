import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from redis import Redis
import utils
import pandas as pd


st.set_page_config(
    page_title = "Audio Similarity Service",
    # page_icon = ,
    # layout = "wide",
    initial_sidebar_state = "collapsed",
)

# workaround to hide side navbar
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """, unsafe_allow_html=True)


# additional styling
# st.markdown("""<style>.css-zt5igj svg{display:none}</style>""", unsafe_allow_html=True)


# set session_state values
if 'song_upload' not in st.session_state:
    st.session_state.song_upload = None
if 'selected_song' not in st.session_state:
        st.session_state.selected_song = None
if 'query_db' not in st.session_state:
    st.session_state.query_db = False
    st.session_state.df = pd.DataFrame()
if 'page_switch' not in st.session_state:
    st.session_state.page_switch = None
st.session_state.page_switch = None


st.title("Audio Similarity")

tab1, tab2 = st.tabs(["Upload File", "Query Database"])

# upload own audio file
with tab1:
    st.header("File Upload")

    upload = st.file_uploader("Upload song", type=["mp3", "wav"], accept_multiple_files=False,
                            key=None, help="Tooltip", on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    if upload:
        st.session_state.song_upload = upload

    # button to show results
    if st.session_state.song_upload:
        if st.button("Show results.", key="button_tab1", use_container_width=True):
            with st.spinner("Loading..."):
                st.session_state.selected_song = None
                switch_page("results")


# redis database search
with tab2:
    st.header("Redis Database Search")

    redis_conn = Redis(host='localhost', port=6379, password=None)

    def get_song_info(id):
        try:
            return f"{st.session_state.df.loc[id, 'track_title']} [{st.session_state.df.loc[id, 'artist_name']}]"
        except:
            return id

    if not st.session_state.query_db:
        with st.spinner(text="Querying database..."):
            st.session_state.df = utils.query_database()
            st.session_state.query_db = True
            st.experimental_rerun()
    else:
        st.write(str(len(st.session_state.df)), "songs found.")
        st.session_state.selected_song = st.selectbox("Search for song in database:", [""]+list(st.session_state.df["track_id"]), format_func=get_song_info)

    # button to show results
    if st.session_state.selected_song:
        if st.button("Show results.", key="button_tab2", use_container_width=True):
            with st.spinner("Loading..."):
                st.session_state.song_upload = None
                switch_page("results")