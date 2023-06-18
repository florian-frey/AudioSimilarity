import streamlit as st
import pandas as pd
import numpy as np
import librosa
import matplotlib.pyplot as plt

st.title("Audio Similarity")

audio = st.file_uploader("Upload song", type=["mp3", "wav"], accept_multiple_files=False, key=None, help="Tooltip", on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

if audio is not None:
    st.write(audio)
    st.audio(audio, format="audio/wav", start_time=0, sample_rate=None)

    # To read file as bytes:
    # bytes_data = audio.getvalue()
    # st.write(bytes_data)

    # To convert to a string based IO:
    # from io import StringIO
    # stringio = StringIO(audio.getvalue().decode("utf-8"))
    # st.write(stringio)
    

    # To read file as string:
    # string_data = stringio.read()
    # st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    # dataframe = pd.read_csv(uploaded_file)
    # st.write(dataframe)

    

    y, sr = librosa.load(audio)
    
    audio_len = len(y) / sr
    timestamps = np.linspace(0, audio_len, num=len(y))

    fig, ax = plt.subplots()
    ax.plot(timestamps, y)
    
    st.pyplot(fig)