import os
import numpy as np
import librosa
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, TimeDistributed, Dense, GlobalAveragePooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# Function to create spectrogram from audio file and save it
def create_and_save_spectrogram(file_path, save_path):
    print(f"Creating spectrogram for {file_path}...")
    y, sr = librosa.load(file_path, sr=None)
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    spectrogram = librosa.power_to_db(spectrogram)
    np.save(save_path, spectrogram)
    print(f"Spectrogram saved to {save_path}")

# Function to create ResNet feature extractor
def create_resnet(input_shape):
    print("Creating ResNet feature extractor...")
    base_model = ResNet50(include_top=False, weights='imagenet', input_shape=input_shape)
    x = base_model.output
    outputs = GlobalAveragePooling2D()(x)
    model = Model(inputs=base_model.input, outputs=outputs)
    return model

# Function to load spectrogram from file and preprocess it
def load_and_preprocess_spectrogram(file_path):
    print(f"Loading and preprocessing spectrogram from {file_path}...")
    spectrogram = np.load(file_path)
    spectrogram = np.repeat(spectrogram[..., np.newaxis], 3, -1)  # ResNet expects 3-channel images
    spectrogram = preprocess_input(spectrogram)
    return spectrogram

# Function to load data
def load_data(spectrogram_directory, audio_directory):
    spectrograms = []
    labels = []
    print(f"Loading data from {spectrogram_directory}...")
    for filename in os.listdir(spectrogram_directory):
        if filename.endswith(".npy"):
            file_path = os.path.join(spectrogram_directory, filename)
            spectrogram = load_and_preprocess_spectrogram(file_path)
            spectrograms.append(spectrogram)
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

# The directory where your test audio files are stored
test_audio_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\testData4'

# The directory where you want to save the test spectrograms
test_spectrogram_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\test_spectrograms'

# Create and save spectrograms for the test set
print("Creating spectrograms for the test set...")
for filename in os.listdir(test_audio_directory):
    if filename.endswith(".wav"):
        file_path = os.path.join(test_audio_directory, filename)
        save_path = os.path.join(test_spectrogram_directory, filename.replace('.wav', '.npy'))
        create_and_save_spectrogram(file_path, save_path)

# Load the test data
print("Loading test data...")
test_spectrograms, test_labels = load_data(test_spectrogram_directory, test_audio_directory)

# Create the ResNet feature extractor
resnet = create_resnet((test_spectrograms.shape[1], test_spectrograms.shape[2], test_spectrograms.shape[3]))

# Extract features using ResNet
print("Extracting features for the test set using ResNet...")
test_features = resnet.predict(test_spectrograms)

# Add an extra dimension for the time steps
test_features = np.expand_dims(test_features, 1)

# Load the trained model
print("Loading the trained model...")
model = load_model('model.h5')

# Predict the labels for the test set
print("Predicting labels for the test set...")
test_pred = np.argmax(model.predict(test_features), axis=-1)

# Compute the confusion matrix, accuracy, and classification report
cm = confusion_matrix(test_labels, test_pred)
acc = accuracy_score(test_labels, test_pred)
report = classification_report(test_labels, test_pred)

# Print the results
print("Confusion Matrix:")
print(cm)
print(f"Accuracy: {acc}")
print("Classification Report:")
print(report)
