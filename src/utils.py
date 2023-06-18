from IPython.display import Audio
import librosa

def display(song):
    return Audio(song)

def load(song):
    y, sr = librosa.load(song)
    return y, sr

def bpm(y, sr=22050):
    bpm, _ = librosa.beat.beat_track(y=y, sr=sr)
    return round(bpm)