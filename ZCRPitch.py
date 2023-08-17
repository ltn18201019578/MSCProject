# Let's modify your code to include energy and fundamental frequency information

import os
import librosa
import numpy as np

# Your target directory
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\test'

# A dictionary to store the measurements for each accent
measurements = {
    0: [],  # northern
    1: [],  # JAC
    2: [],  # southwestern
    3: [],  # northwestern
    4: [],
    5: [],
}

n = 0
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        n = n+1
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

            # Compute Zero Crossing Rate
            zcr = librosa.feature.zero_crossing_rate(y)
            avg_zcr = np.mean(zcr)

            # Compute pitch contour
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_std = np.std(pitches)

            # Compute RMS energy
            rms = librosa.feature.rms(y=y)
            avg_rms = np.mean(rms)

            # Compute fundamental frequency
            f0 = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
            avg_f0 = np.mean(f0)

            # Add the measurements to the dictionary
            measurements[accent].append((avg_zcr, pitch_std, avg_rms, avg_f0))
            print(n)

# Compute the average for each accent
averages = {}
for accent, values in measurements.items():
    avg_zcr = np.mean([v[0] for v in values])
    avg_pitch_std = np.mean([v[1] for v in values])
    avg_rms = np.mean([v[2] for v in values])
    avg_f0 = np.mean([v[3] for v in values])
    averages[accent] = (avg_zcr, avg_pitch_std, avg_rms, avg_f0)

# Print the averages
for accent, (avg_zcr, avg_pitch_std, avg_rms, avg_f0) in averages.items():
    print(f"Accent: {accent}, Average ZCR: {avg_zcr}, Average pitch std: {avg_pitch_std}, Average RMS: {avg_rms}, Average F0: {avg_f0}")
