import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from redis import Redis
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import VectorField, TagField, TextField, NumericField


###                     ###
###      Database       ###
###                     ###

def query_database(page_start=0, page_end=8000):
        base_query = f'*'
        query = Query(base_query)\
            .sort_by("track_title")\
            .paging(page_start, page_end)\
            .dialect(2)
        
        results = Redis(host="localhost", port=6379, password=None).ft("audiosimilarity").search(query)

        df = pd.DataFrame(list(map(lambda x: x.__dict__, results.docs)))
        df["track_id"] = df["id"].str[16:]
        df.index = df["track_id"]

        return df


def get_vector_similarity(vec:np.array, n_songs:int=5):

    base_query = f'* =>[ KNN {n_songs} @feature_vector $vec_param AS vector_score]'

    query = Query(base_query)\
        .sort_by("vector_score", asc=False)\
        .dialect(2)

    params_dict = {"vec_param": vec.astype(dtype=np.float32).tobytes()}

    results = Redis(host="localhost", port=6379, password=None).ft("audiosimilarity").search(query, params_dict)

    return pd.DataFrame(list(map(lambda x: x.__dict__, results.docs)))



###                     ###
###      Feature        ###
###     Extraction      ###
###                     ###

import librosa
import matplotlib.pyplot as plt


def create_melspectrogram(y: np.ndarray, sr: int, output_file: str, array_path: str = None):
    """
        Args:
            y : np.ndarray [shape=(..., n)] or None
                audio time-series. Multi-channel is supported.
            sr : number > 0 [scalar]
                sampling rate of ``y``
            output_file: str or pathlib.Path
                file to store the diagram
    """
    
    if not os.path.exists(os.path.dirname(output_file)):
      os.makedirs(os.path.dirname(output_file))
    # melspectrogram_array = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,fmax=8000)
    melspectrogram_array = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=512)

    mel = librosa.power_to_db(melspectrogram_array)
    # Length and Width of Spectogram
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = float(mel.shape[1] / 100)
    fig_size[1] = float(mel.shape[0] / 100)
    plt.rcParams["figure.figsize"] = fig_size
    plt.axis('off')
    plt.axes([0., 0., 1., 1.0], frameon=False, xticks=[], yticks=[])
    librosa.display.specshow(mel)   # ,cmap='gray_r'
    plt.savefig(output_file, dpi=100)
    plt.close()
    if array_path is not None:
      np.save(array_path, melspectrogram_array)
    return melspectrogram_array


###                     ###
###     Spotify API     ###
###                     ###

import requests


def get_spotify_id(title, artist):

    # get client id and secret at https://developer.spotify.com/dashboard -> project -> settings
    # store secret in the secret.txt file (DO NOT PUSH TO GITHUB)
    client_id = "fccc6625feab4a0e818cd573c10e00ed"
    with open('secret.txt') as f:
        client_secret = f.readline()

    # receive bearer token, valid for one hour
    response = requests.request("POST",
                                f"https://accounts.spotify.com/api/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}",
                                headers={"Content-Type": "application/x-www-form-urlencoded"}
                                )
    if response.status_code != 200:
        return Exception(response.status_code, response.text)

    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    
    # replace # to prevent API response exception
    title = title.replace("#", "")
    artist = artist.replace("#", "")
    url = f"https://api.spotify.com/v1/search?q=track:{title}%20artist:{artist}&type=track&limit=1"

    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        return Exception(response.status_code, response.text)

    # take first result if any or return None
    try:
        return response.json()["tracks"]["items"][0]["id"]
    except:
        return None
