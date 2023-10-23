import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import os 

def load_class_names():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    class_map_path = os.path.join(current_directory, 'yamnet_class_map.csv')
    class_names = pd.read_csv(class_map_path, sep=',', usecols=[2], skipinitialspace=True).values.squeeze().tolist()
    
    #class_map_path = "yamnet_class_map.csv"
    #class_names = pd.read_csv(class_map_path, sep=',', usecols=[2], skipinitialspace=True).values.squeeze().tolist()
    
    return class_names

# cargamos el modelo
model = hub.load('https://tfhub.dev/google/yamnet/1')
class_names = load_class_names()

def classify_sound(audio_file_path, top_n=4):
    # tf.io.read_file(audio_file_path) lee el archivo de audio
    # tf.audio.decode_wav() toma el contenido del audio y lo decodifica para que TensorFlow pueda usarlo
    waveform, sample_rate = tf.audio.decode_wav(tf.io.read_file(audio_file_path), desired_channels=1)

    # ajusta el formato
    waveform = tf.squeeze(waveform, axis=-1)

    # scores son las puntuaciones para cada posible categoría detectada por YAMNet
    scores, _, _ = model(waveform)  # Aquí agregamos la línea para calcular scores

    # Ordena las puntuaciones de mayor a menor y toma los primeros top_n índices
    top_indices = scores.numpy().mean(axis=0).argsort()[-top_n:][::-1]
    
    # Obtiene las etiquetas y puntuaciones correspondientes
    top_labels = [class_names[i] for i in top_indices]
    top_scores = [scores.numpy().mean(axis=0)[i] for i in top_indices]

    return top_labels, top_scores