# import os
import requests
import pandas as pd
import numpy as np
# from tqdm import tqdm
from redis import Redis
from redis.commands.search.query import Query


###                     ###
###      Database       ###
###                     ###

def query_database(page_start=0, page_end=8000):
        base_query = f'*'
        query = Query(base_query)\
            .sort_by("track_title")\
            .paging(page_start, page_end)\
            .dialect(2)
        
        try:
            results = Redis(host="database", port=6379, password=None).ft("audiosimilarity").search(query)
        except:
            results = Redis(host="localhost", port=6379, password=None).ft("audiosimilarity").search(query)

        df = pd.DataFrame(list(map(lambda x: x.__dict__, results.docs)))
        df["track_id"] = df["id"].str[16:]
        df.index = df["track_id"]

        return df


def get_vector_similarity(vec:np.array, n_songs:int=50):

    base_query = f'* =>[ KNN {n_songs} @feature_vector $vec_param AS vector_score]'

    query = Query(base_query)\
        .sort_by("vector_score", asc=False)\
        .paging(0, n_songs)\
        .dialect(2)

    params_dict = {"vec_param": vec.astype(dtype=np.float32).tobytes()}

    try:
        results = Redis(host="database", port=6379, password=None).ft("audiosimilarity").search(query, params_dict)
    except:
        results = Redis(host="localhost", port=6379, password=None).ft("audiosimilarity").search(query, params_dict)

    return pd.DataFrame(list(map(lambda x: x.__dict__, results.docs)))



###                     ###
###      Feature        ###
###     Extraction      ###
###                     ###

# import librosa
# import matplotlib.pyplot as plt

def extract_features(audio):
    # ...
    return feature_vector


###                     ###
###     Spotify API     ###
###                     ###



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
