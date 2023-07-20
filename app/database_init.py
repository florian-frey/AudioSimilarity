import pandas as pd
import numpy as np
from tqdm import tqdm
from redis import Redis
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import VectorField, TextField, NumericField


index_name = "audiosimilarity"
distance_metric:str="COSINE"
DIM = 100

# load data
df = pd.read_csv("../fma-metadata/tracks_small.csv", index_col=0, header=[0,1])

# redis connection
redis_conn = Redis(host='localhost', port=6379, password=None)


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

feature_vector = VectorField("feature_vector",
            "HNSW", {
                "TYPE": "FLOAT32",
                "DIM": DIM,
                "DISTANCE_METRIC": distance_metric,
                "INITIAL_CAP": 10000,
            })

# create index
redis_conn.ft(index_name).create_index(
    fields = [track_title, album_title, artist_name, track_publisher, album_tracks, bit_rate, duration, genre_top, language_code, album_date_released, feature_vector],
    definition = IndexDefinition(prefix=[index_name], index_type=IndexType.HASH)
)

print("Index created.")
print("Populating database... May take a few minutes.")

# populate database
for track_id, row in tqdm(df.iloc[:,:].iterrows()):

    row = row.replace({pd.NaT: "null"})

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
            "feature_vector": np.random.rand(DIM).astype(dtype=np.float32).tobytes()
        }
    )


print("Database ready. Starting app...")