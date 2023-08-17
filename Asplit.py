import librosa
import os
import numpy as np
from scipy.io import wavfile

input_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\last\train'
output_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\last\trainSplit'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for filename in os.listdir(input_directory):
    if filename.endswith('.wav'):
        file_path = os.path.join(input_directory, filename)
        y, sr = librosa.load(file_path, sr=None)
        y_trimmed, _ = librosa.effects.trim(y, top_db=20)  # trim the silent parts with a threshold of 20 dB
        y_trimmed_int16 = (y_trimmed * 32767).astype(np.int16)  # Convert to int16 format
        output_path = os.path.join(output_directory, filename)
        wavfile.write(output_path, sr, y_trimmed_int16)  # Save the trimmed file to the new directory
        print(f"Processed and saved: {output_path}")
