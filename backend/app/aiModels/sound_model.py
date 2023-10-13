import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd 

def load_class_names():
    class_map_path = "yamnet_class_map.csv"
    class_names = pd.read_csv(class_map_path, sep=',', usecols=[2], skipinitialspace=True).values.squeeze().tolist()
    return class_names

# cargamos el modelo
model = hub.load('https://tfhub.dev/google/yamnet/1')
class_names = load_class_names()

def classify_sound(audio_file_path):
    # tf.io.read_file(audio_file_path) lee el archivo de audio
    # tf.audio.decode_wav() toma el contenido del audio y lo decodifica para que TensorFlow pueda usarlo
    waveform, sample_rate = tf.audio.decode_wav(tf.io.read_file(audio_file_path), desired_channels=1)

    # ajusta el formato
    waveform = tf.squeeze(waveform, axis=-1)

    # scores son las puntuaciones para cada posible categoría detectada por YAMNet
    scores, embeddings, log_mel_spectogram = model(waveform)

    # calcula la media de las puntuaciones y nos da la que tiene mayor índice
    prediction = class_names[scores.numpy().mean(axis=0).argmax()]
    
    return prediction

audio_file_path = "D:\\BOOTCAMPF5\\SoundOfSilence\\audio2.wav"


label = classify_sound(audio_file_path)
print(f"The predicted label for the audio is: {label}")