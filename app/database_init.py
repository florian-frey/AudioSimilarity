import zipfile
import json
import pandas as pd
import numpy as np
from time import sleep
from tqdm import tqdm
from redis import Redis
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import VectorField, TextField, NumericField


index_name = "audiosimilarity"
distance_metric:str="COSINE"
DIM = 1000

# load data
print("Extracting and reading data...")
with zipfile.ZipFile("tracks_small.zip", 'r') as zip_ref:
        zip_ref.extractall("./")
with zipfile.ZipFile("vectors_test_data.zip", 'r') as zip_ref:
    zip_ref.extractall("./")
metadata = pd.read_csv("tracks_small.csv", index_col=0, header=[0,1])
vectors = pd.read_csv("vectors_test_data.csv", index_col=0, header=[0,1], sep=",")
df = pd.merge(metadata, vectors, left_index=True, right_index=True)

# redis connection
redis_conn = Redis(host='database', port=6379, password=None)


# define fields
track_title = TextField(name="track_title")
album_title = TextField(name="album_title")
artist_name = TextField(name="artist_name")
track_publisher = TextField(name="track_publisher")

album_tracks = NumericField(name="album_tracks")
bit_rate = NumericField(name="bit_rate")
duration = NumericField(name="duration")
genre_top = TextField(name="genre_top")

language_code = TextField(name="language_code")
album_date_released = TextField(name="album_date_released")

feature_vector_text = TextField(name="feature_vector_text")
feature_vector = VectorField("feature_vector",
            "HNSW", {
                "TYPE": "FLOAT32",
                "DIM": DIM,
                "DISTANCE_METRIC": distance_metric,
                "INITIAL_CAP": 10000,
            })

# create index
for retry in range(1,6):
    print("Connecting to database...")
    try:
        redis_conn.ft(index_name).create_index(
            fields = [track_title, album_title, artist_name, track_publisher, album_tracks, bit_rate, duration, genre_top, language_code, album_date_released, feature_vector_text, feature_vector],
            definition = IndexDefinition(prefix=[index_name], index_type=IndexType.HASH)
        )
        break
    except:
        print(f"Connection failed. Retrying in {5*retry} seconds...")
        sleep(5*retry)


print("Index created.")
print("Populating database... May take a few minutes.")

# populate database
for track_id, row in tqdm(df.iloc[:,:].iterrows()):

    row = row.replace({pd.NaT: "null"})

    feature_vector_text = row["feature", "vector"]
    feature_vector = np.array(json.loads(feature_vector_text))

    redis_conn.hset(
        f"{index_name}:{track_id}",
        mapping={
            "track_title": row["track", "title"],
            "album_title": row["album", "title"],
            "artist_name": row["artist", "name"],
            "track_publisher": row["track", "publisher"],
            "album_tracks":  row["album", "tracks"],
            "bit_rate": row["track", "bit_rate"],
            "duration": row["track", "duration"],
            "genre_top": row["track", "genre_top"],
            "language_code": row["track", "language_code"],
            "album_date_released": row["album", "date_released"],
            "feature_vector_text": feature_vector_text,
            "feature_vector": feature_vector.astype(dtype=np.float32).tobytes()
        }
    )


print("Database ready. Starting app...")