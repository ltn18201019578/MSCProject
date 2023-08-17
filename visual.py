import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

# Your target directory
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\undersampled_data'

volumes = []  # List to store the volumes
n = 0
# Loop over all audio files
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        n = n + 1
        print(n)
        file_path = os.path.join(directory, filename)
        y, sr = librosa.load(file_path)
        rms = librosa.feature.rms(y=y)
        avg_rms = np.mean(rms)
        volumes.append(avg_rms)

# Plot histogram of volumes
plt.hist(volumes, bins=50)
plt.xlabel('Volume')
plt.ylabel('Number of audio files')
plt.title('Distribution of volumes across audio files')
plt.show()