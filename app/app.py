import streamlit as st
# from st_pages import Page, show_pages, add_page_title, hide_pages
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
from redis import Redis
from redis.commands.search.query import Query
import utils



st.set_page_config(
    page_title = "Audio Similarity Service",
    # page_icon = ,
    # layout = "wide",
    initial_sidebar_state = "collapsed",
    # menu_items = {
    #     "Get Help": None,
    #     "Report a Bug": None,
    #     "About": None
    # }
)
# workaround to hide side navbar
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
st.session_state.page = 0


st.title("Audio Similarity")


tab1, tab2 = st.tabs(["Upload File", "Query Database"])

with tab1:

    # upload own audio file
    st.header("File Upload")

    upload = st.file_uploader("Upload song", type=["mp3", "wav"], accept_multiple_files=False,
                            key=None, help="Tooltip", on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    if upload:
        st.session_state.song_upload = upload

     # button to show results
    if st.session_state.song_upload:
        if st.button("Show results.", key="button_upload"):
            with st.spinner("Loading..."):
                st.session_state.selected_song = None
                switch_page("results")


with tab2:
# redis database search

    redis_conn = Redis(host='localhost', port=6379, password=None)

    st.header("Redis Database Search")

    def get_song_info(id):
        try:
            return f"{st.session_state.df.loc[id, 'track_title']} [{st.session_state.df.loc[id, 'artist_name']}]"
        except:
            return id

    if not st.session_state.query_db:
        # if st.button("Query Database"):
            with st.spinner(text="Querying database..."):
                st.session_state.df = utils.query_database()
                st.session_state.query_db = True
                st.experimental_rerun()
    else:
        st.write(str(len(st.session_state.df)), "songs found.")
        st.session_state.selected_song = st.selectbox("Search for song in database:", [""]+list(st.session_state.df["track_id"]), format_func=get_song_info)

    # button to show results
    if st.session_state.selected_song:
        if st.button("Show results.", key="button_select"):
            with st.spinner("Loading..."):
                st.session_state.song_upload = None
                switch_page("results")