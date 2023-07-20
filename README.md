# AudioSimilarity

## Running Dev Environment

To start the redis database run

```
docker run -d --name redis-stack -p 6379:6379 redis/redis-stack-server:latest
```

To populate it with our data run the `src/redis.ipynb` notebook.

The Streamlit app can be started by navigating into the `app/` directory and running

```
streamlit run app.py
```

## Running the Project with Docker (used for production)

To build and run the Docker containers, run the following command in the project's root directory:

```
docker-compose up -d --build
```

To run without building (when already built) use the command without the --build-argument:

```
docker-compose up -d
```

To stop the containers from running, use the following command:

```
docker-compose down
```

If additionally the removal of created volumes is desired, add the argument -v:

```
docker-compose down -v
```

## Notebooks & Links

- Autoencoder + CVAE Training und Visualisierung: https://colab.research.google.com/drive/1IAgiIvzWHrfhQIiMLNpzWo-Ve6cmGoL0?usp=sharing

- Spectrogramm Preprocessing ASS: https://colab.research.google.com/drive/1PFnOeIdPzhg9vUTvK_k_A7_otIBDVGNZ?usp=sharing

- CNN Genre Classifier: https://colab.research.google.com/drive/1BwaHqNcPWjuwzE0ey5j44oEu1CVrcMFv?usp=sharing

- Load Model an Test it: https://colab.research.google.com/drive/1ZhmiyUJKo7o4vtH8D0gQXfcbNm3OfZ2c?usp=sharing

- dataset link: https://drive.google.com/drive/folders/1vcdYV2ROD2mog9uNa9soXa1xsQ_dT7dc?usp=sharing

- Model link: https://drive.google.com/drive/folders/1EmKaHxKsIM6hl1tTY2dVYQvHCcY7koNc?usp=sharing

- Model Evaluation: https://colab.research.google.com/drive/1frIrlznYXRoXgIe9ZZZ5O0jClbYJKc6O?usp=sharing

## Datenquellen

https://www.kaggle.com/datasets/tpapp157/billboard-hot-100-19602020-spectrograms
5737 Spectrogramme

https://zenodo.org/record/5794629
3000 artificial audio tracks

https://github.com/mdeff/fma
106.574 audio tracks

https://github.com/MTG/melon-music-dataset
649.091 spectrogramme und metadaten
(koreanisch)

### FMA (free music archive)

Benchmark for genre classification and Description: https://paperswithcode.com/dataset/fma#:~:text=The%20Free%20Music%20Archive%20%28FMA%29%20is%20a%20large-scale,arranged%20in%20a%20hierarchical%20taxonomy%20of%20161%20genres.

Kaggle: https://www.kaggle.com/datasets/imsparsh/fma-free-music-archive-small-medium
(sample Classification achieves 46% accuracy)

### Last.fm

Million Song dataset with other enriched (like Last.fm):
https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm

Music Recommandation Notebook with Last.fm:
https://www.kaggle.com/code/pcbreviglieri/recommending-music-artists-with-boltzmann-machines/notebook

### Audio similarity Deep Learning:

Musical Audio Similarity with Self-supervised Convolutional Neural Networks
https://arxiv.org/abs/2202.02112

Audio-based Near-Duplicate Video Retrieval with Audio Similarity Learning
https://github.com/mever-team/ausil
