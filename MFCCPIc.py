import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load the audio file
file_path = r'C:\Users\18201\OneDrive\桌面\study\final project\trainData4\20170001P00001I0001.wav'
y, sr = librosa.load(file_path)

# Compute the 13-dimensional MFCC
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

# Display the MFCCs
plt.figure(figsize=(10, 6))
librosa.display.specshow(mfccs, sr=sr, x_axis='time')
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()
plt.show()
