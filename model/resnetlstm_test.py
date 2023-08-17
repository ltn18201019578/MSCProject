import os
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

def load_data(spectrogram_directory,audio_directory):
    spectrograms = []
    labels = []  # Assuming you have a way to get corresponding labels
    print(f"Loading data from {spectrogram_directory}...")
    for filename in os.listdir(spectrogram_directory):
        if filename.endswith(".npy"):
            file_path = os.path.join(spectrogram_directory, filename)
            spectrogram = np.load(file_path)
            spectrogram = np.repeat(spectrogram[..., np.newaxis], 3, -1)  # ResNet expects 3-channel images
            spectrogram = preprocess_input(spectrogram)
            spectrograms.append(spectrogram)
            # Add corresponding label (modify this part as needed)
            metadata_file = os.path.join(audio_directory, filename.replace('.npy', '.metadata'))
            try:
                with open(metadata_file, 'r', encoding='UTF-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(metadata_file, 'r', encoding='gbk') as f:
                    content = f.read()
            accent_line = next(line for line in content.split('\n') if line.startswith('BIR'))
            label = int(accent_line.split(' ')[1])
            labels.append(label)
    return np.array(spectrograms), np.array(labels)

# The directory where your test spectrogram files are stored
test_spectrogram_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\test_spectrograms'
test_audio_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\testData4'  # Assuming test metadata is in the same directory

# Load the test data
test_spectrograms, test_labels = load_data(test_spectrogram_directory, test_audio_directory)

# Load the trained model
model_path = 'AverLST40.h5'
model = load_model(model_path)

# Predict labels for the test data
predicted_labels = model.predict(test_spectrograms)
predicted_labels = np.argmax(predicted_labels, axis=1)  # Convert from one-hot encoding to class labels

# Compute and print the confusion matrix
conf_matrix = confusion_matrix(test_labels, predicted_labels)
print("Confusion Matrix:")
print(conf_matrix)
