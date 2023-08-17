import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

# Your target directory
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\train_data'

# The directory to save the spectrograms
output_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\spectrograms'

for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        # Get the full path of the file
        file_path = os.path.join(directory, filename)

        # Load the audio file
        y, sr = librosa.load(file_path)

        # Compute the spectrogram
        D = librosa.stft(y)

        # Convert the spectrogram to decibels for visualization
        D_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

        # Plot the spectrogram
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(D_db, sr=sr, x_axis='time', y_axis='log')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Spectrogram of ' + filename)

        # Save the figure to a file
        output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.png')
        plt.savefig(output_file_path)
        plt.close()
