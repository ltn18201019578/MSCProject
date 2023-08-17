import os
import librosa
import numpy as np
import soundfile as sf
import shutil  # Import shutil module

# Function to change speed of audio data
def change_speed(data, speed_factor):
    return librosa.effects.time_stretch(y=data, rate=speed_factor)

# Function to change pitch of audio data
def change_pitch(data, sr, pitch_factor):
    return librosa.effects.pitch_shift(y=data, sr=sr, n_steps=pitch_factor)

# Function to change volume of audio data
def change_volume(data, volume_factor):
    return data * volume_factor

# Your target directory
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\testData4'
output_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\newTestData4'

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

n = 0
# Loop over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        # Get the full path of the file
        file_path = os.path.join(directory, filename)
        base_name = os.path.splitext(filename)[0]
        metadata_file = os.path.join(directory, base_name + ".metadata")

        # Read the accent from the metadata file
        with open(metadata_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        accent = None
        for line in lines:
            if line.startswith('BIR'):
                accent = int(line.split(' ')[1])
                break

        if accent is not None:
            # Load the audio file
            y, sr = librosa.load(file_path)
            n = n + 1
            print(n)

            # Define the modification factors based on the accent
            if accent == 0:  # Northern
                y_changed = change_speed(y, 1.1)

            elif accent == 1:  # JAC
                y_changed = y

            elif accent == 2:  # Southwestern
                y_changed = y
            elif accent == 3:  # Northwestern
                y_changed = y
            elif accent == 4:  # Northwestern
                y_changed = y
            elif accent == 5:  # Northwestern
                y_changed = y
            else:
                continue

            # Apply the modifications


            # Define the path of the output file
            output_path = os.path.join(output_directory, filename)

            # Save the modified audio to a .wav file
            sf.write(output_path, y_changed, sr)

            # Copy the metadata file to the new directory
            shutil.copy(metadata_file, output_directory)
