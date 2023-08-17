import os
import librosa
import numpy as np
import soundfile as sf

# Your target directory
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\last\testSplit'

# The target length in seconds
target_length_s = 2.4
n = 0
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        # Get the full path of the file
        file_path = os.path.join(directory, filename)

        # Load the audio file
        y, sr = librosa.load(file_path, sr=None)

        # The target length in samples
        target_length = int(target_length_s * sr)

        if len(y) < target_length:
            # If the audio is shorter than the target length, pad it with zeros
            y = np.pad(y, (0, target_length - len(y)), 'constant')
        else:
            # If the audio is longer than the target length, truncate it
            y = y[:target_length]


        # Save the modified audio back to the file
        sf.write(file_path, y, sr)
        n = n + 1
        print(n)
