import os
import numpy as np
import librosa
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import LSTM, TimeDistributed, Dense, GlobalMaxPooling2D,GlobalAveragePooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import Conv2D, concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.layers import GlobalAveragePooling2D
# Function to create ResNet feature extractor
def create_resnet(input_shape):
    print("Creating ResNet feature extractor...")
    base_model = ResNet50(include_top=False, weights='imagenet', input_shape=input_shape)
    x = base_model.output
    outputs = GlobalAveragePooling2D()(x)
    model = Model(inputs = base_model.input, outputs = outputs)
    return model
# Function to load spectrogram from file and preprocess it
def load_and_preprocess_spectrogram(file_path):
    print(f"Loading and preprocessing spectrogram from {file_path}...")
    spectrogram = np.load(file_path)
    spectrogram = np.repeat(spectrogram[..., np.newaxis], 3, -1)  # ResNet expects 3-channel images
    spectrogram = preprocess_input(spectrogram)
    return spectrogram

# Function to load data
def load_data(spectrogram_directory):
    spectrograms = []
    filenames = []  # Store the filenames in the order they are loaded
    print(f"Loading data from {spectrogram_directory}...")
    for filename in os.listdir(spectrogram_directory):
        if filename.endswith(".npy"):
            file_path = os.path.join(spectrogram_directory, filename)
            spectrogram = load_and_preprocess_spectrogram(file_path)
            spectrograms.append(spectrogram)
            filenames.append(filename)  # Add filename to the list
    return np.array(spectrograms), filenames  # Return filenames along with spectrograms

# The directory where your audio files are stored
audio_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\trainData4'

# The directory where you want to save the spectrograms
spectrogram_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\spectrograms'

# The directory where you want to save the ResNet features
resnet_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\resnetAverNewTrain'

# Load the data
spectrograms, filenames = load_data(spectrogram_directory)  # Save filenames when loading data

# Create the ResNet feature extractor
resnet = create_resnet((spectrograms.shape[1], spectrograms.shape[2], spectrograms.shape[3]))

# Extract features using ResNet
print("Extracting features using ResNet...")
features = resnet.predict(spectrograms)
features = np.expand_dims(features, 1)

# Save the features
print("Saving ResNet features...")
for i, filename in enumerate(filenames):  # Use saved filenames when saving features
    save_path = os.path.join(resnet_directory, filename)  # Save feature with the same filename as the corresponding spectrogram
    np.save(save_path, features[i])
