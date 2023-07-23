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

- Datasets:
  - 3 seconds melspectrograms, spectral contrast, chroma stft dataset link: https://drive.google.com/file/d/12H5OzHtYo9DmRXdRV7DNqZhkG7kZk2Hf/view?usp=sharing
  - 3 seconds all spectrograms stacked together: https://drive.google.com/file/d/18HGpYe5eF_4bNlqZX-gOVY5jqfK0uUGT/view?usp=sharing
  - 30 seconds melspectrograms dataset link: https://drive.google.com/drive/folders/1vcdYV2ROD2mog9uNa9soXa1xsQ_dT7dc?usp=sharing
  - Predicted vectors test data: https://drive.google.com/file/d/1--CheDCvqEwBvr4f_3aJW8dpVpM9WB_U/view?usp=sharing

- Link to Models: https://drive.google.com/drive/folders/1EmKaHxKsIM6hl1tTY2dVYQvHCcY7koNc?usp=sharing

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
