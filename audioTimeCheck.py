import os
import librosa

# Your audio files directory
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\last\trainSplit'

total_length = 0
count = 0

for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        # Get the full path of the audio file
        audio_file_path = os.path.join(directory, filename)

        # Load the audio file
        y, sr = librosa.load(audio_file_path, sr=16000)

        # Add the length of this audio file to the total length
        total_length += len(y) / sr  # The length of the audio file in seconds
        count += 1

# Calculate the average length
average_length = total_length / count

print("Average length of audio files: {} seconds".format(average_length))
