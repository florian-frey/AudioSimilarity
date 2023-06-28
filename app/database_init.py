import pandas as pd
import psycopg2
import zipfile
from time import sleep
from tqdm import tqdm
import toml


secrets = toml.load("/code/.streamlit/secrets.toml")["connections"]["postgres"]

for retry in range(1,6):
    print("Connecting to database...")
    try:
        conn = psycopg2.connect(f"host={secrets['host']} port={secrets['port']} dbname={secrets['database']}  user={secrets['username']}  password={secrets['password']}")
        cursor = conn.cursor()
        break
    except:
        print(f"Retrying in {5*retry} seconds...")
        sleep(5*retry)

cursor.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = 'tracks');")
if cursor.fetchone()[0]:
    print("Table 'tracks' already exists.")
    cursor.close()
    conn.close()

else:
    print("Extracting Files...")

    # read and preprocess metadata
    with zipfile.ZipFile("tracks.zip", 'r') as zip_ref:
        zip_ref.extractall("./")

    data = pd.read_csv("tracks.csv", index_col=0, header=[0, 1])

    data[("album", "date_created")] = pd.to_datetime(data[("album", "date_created")])
    data[("album", "date_released")] = pd.to_datetime(data[("album", "date_released")])

    data[("track", "date_created")] = pd.to_datetime(data[("track", "date_created")])
    data[("track", "date_recorded")] = pd.to_datetime(data[("track", "date_recorded")])

    data = data.dropna(subset=[("track", "title")])


    # write data to db
    print("Initializing database (may take a few minutes)...")

    cursor.execute("""
        CREATE TABLE tracks (
            track_id            INT PRIMARY KEY,
            track_title         VARCHAR NOT NULL,
            track_bit_rate      INT,
            track_date_recorded DATE,
            track_duration      INT,
            track_genre_top     VARCHAR,
            track_genres        VARCHAR,
            track_language_code VARCHAR,
            track_tags          VARCHAR,
            track_publisher     VARCHAR,
            album_title         VARCHAR,
            album_tracks        INT,
            album_type          VARCHAR,
            album_date_released DATE,
            artist_name         VARCHAR,
            artist_location     VARCHAR
            )
                """)

    for idx, row in tqdm(data.iterrows()):
        row = row.replace({pd.NaT: None})
        cursor.execute('''
                    INSERT INTO tracks (track_id, track_title, track_bit_rate, track_date_recorded, track_duration, track_genre_top,
                    track_genres, track_language_code, track_tags, track_publisher, album_title, album_tracks, album_type, album_date_released,
                    artist_name, artist_location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                    ''',
                    (
                    idx,
                    row["track", "title"],
                    row["track", "bit_rate"],
                    row["track", "date_recorded"],
                    row["track", "duration"],
                    row["track", "genre_top"],
                    row["track", "genres"],
                    row["track", "language_code"],
                    row["track", "tags"],
                    row["track", "publisher"],
                    row["album", "title"],
                    row["album", "tracks"],
                    row["album", "type"],
                    row["album", "date_released"],
                    row["artist", "name"],
                    row["artist", "location"]
                    ))

    conn.commit()
    cursor.close()
    conn.close()