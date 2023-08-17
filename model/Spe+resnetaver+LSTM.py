import os
import numpy as np
import librosa
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import LSTM, TimeDistributed, Dense, GlobalAveragePooling2D,GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

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


# The directory where your audio files are stored
audio_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\trainData4'

# The directory where you want to save the spectrograms
spectrogram_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\spectrograms'

#Create and save spectrograms
for filename in os.listdir(audio_directory):
    if filename.endswith(".wav"):
        file_path = os.path.join(audio_directory, filename)
        save_path = os.path.join(spectrogram_directory, filename.replace('.wav', '.npy'))
        create_and_save_spectrogram(file_path, save_path)

# Load the data
spectrograms, labels = load_data(spectrogram_directory, audio_directory)

# Create the ResNet feature extractor
resnet = create_resnet((spectrograms.shape[1], spectrograms.shape[2], spectrograms.shape[3]))

# Extract features using ResNet
print("Extracting features using ResNet...")
features = resnet.predict(spectrograms)

# Add an extra dimension for the time steps
features = np.expand_dims(features, 1)
print(f"Features shape: {features.shape}")

# Create the LSTM model
print("Creating LSTM model...")
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(features.shape[1], features.shape[2])))
model.add(LSTM(64))
model.add(Dense(4, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
print("Training model...")
model.fit(features, labels, epochs=10, validation_split=0.2)
model.save('model.h5')
print("Model trained and saved to model.h5")
