import os
import librosa
import numpy as np

# Your target directory
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\last\testSplit'
output_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\last\testSplitMFCC'

n = 0
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        n = n+1
        # Get the full path of the file
        file_path = os.path.join(directory, filename)

        # Load the audio file
        y, sr = librosa.load(file_path)

        # Compute MFCC features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

        # Compute Frequency Energy
        # rms = librosa.feature.rms(y=y)[0]

        # Compute Zero Crossing Rate
        # zcr = librosa.feature.zero_crossing_rate(y)[0]

        # Compute Subband Power
        # subband_power = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=0)

        # Compute Frequency Centroid
        # freq_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

        # Compute Bandwidth
        # bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]

        # Compute Pitch Frequency (Fundamental Frequency) for each frame
        # pitch_frequency = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))[0]

        # Stack features together
        features = np.vstack((mfcc))

        # Get the base name of the file (without the extension)
        base_name = os.path.splitext(filename)[0]

        # Define the path of the output file
        # output_path = os.path.join(directory, base_name + ".npy")
        output_path = os.path.join(output_directory, base_name + ".npy")  # Changed to output_directory

        # Save the combined features to a .npy file
        np.save(output_path, features)
        print(n)
