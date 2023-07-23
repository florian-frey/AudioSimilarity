import os
import cv2
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa
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


def extract_features(audio, encoder):

    y, sr = librosa.load(audio)

    # create 30 seconds snippet
    if len(y)//sr < 30:
        # if file shorter than 30 seconds, padding with zeros
        new_array_30_secs = np.zeros(sr*30)
        new_array_30_secs[:len(y)] = y
    else:
        # extract middle 30 seconds of file
        middle = len(y)//2
        start = middle - int(sr*15)
        end = middle + int(sr*15)
        new_array_30_secs = y[start:end]

    # create temporary file for spectrogram
    tmp_file = f"./tmp/{audio.name}.jpg"
    if not os.path.exists(os.path.dirname(tmp_file)):
        os.makedirs(os.path.dirname(tmp_file))

    # create mel-spectrogram
    melspectrogram_array = librosa.feature.melspectrogram(y=new_array_30_secs, sr=sr, n_fft=2048, hop_length=512)
    mel = librosa.power_to_db(melspectrogram_array)
    # Length and Width of Spectogram
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = float(mel.shape[1] / 100)
    fig_size[1] = float(mel.shape[0] / 100)
    plt.rcParams["figure.figsize"] = fig_size
    plt.axis('off')
    plt.axes([0., 0., 1., 1.0], frameon=False, xticks=[], yticks=[])
    # librosa.display.specshow(mel)   # ,cmap='gray_r'
    plt.savefig(tmp_file, dpi=100)
    plt.close()


    # read mel-spectrogram
    melspectrogram_resized = cv2.imread(tmp_file)[:, :1280, :]

    # encode spectrogram to receive feature vector
    feature_vector = []
    for counter in range(10):
      feature_vector.extend(encoder.predict(melspectrogram_resized[:, counter*128:(counter+1)*128, :].reshape(-1, 128, 128, 3), verbose=0))

    # remove temporary file
    os.remove(tmp_file)
    
    return np.array(feature_vector)



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
