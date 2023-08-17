import os
import numpy as np
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dropout
from tensorflow.keras.regularizers import l2

# Function to load ResNet features from file
def load_features(file_path):
    print(f"Loading ResNet features from {file_path}...")
    features = np.load(file_path)
    return features

# Function to load features and labels
def load_features_and_labels(resnet_directory, audio_directory):
    features = []
    labels = []
    print(f"Loading data from {resnet_directory}...")
    for filename in os.listdir(resnet_directory):
        if filename.endswith(".npy"):
            file_path = os.path.join(resnet_directory, filename)
            feature = load_features(file_path)
            features.append(feature)
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
    return np.array(features), np.array(labels)

# The directory where your audio files are stored
audio_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\trainData4'

# The directory where your ResNet features are stored
resnet_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\resnetAver'

# Load the features and labels
features, labels = load_features_and_labels(resnet_directory, audio_directory)

# Add an extra dimension for the time steps
print(f"Features shape: {features.shape}")

# Create the LSTM model
print("Creating LSTM model...")
model = Sequential()
model.add(LSTM(256, return_sequences=True, input_shape=(features.shape[1], features.shape[2])))
model.add(LSTM(128))
model.add(Dense(64, activation='relu'))  # Dense layer
model.add(Dense(4, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Train the model
print("Training model...")
model.fit(features, labels, epochs=100, validation_split=0.2)
model.save('modelAverLSTM256128100.h5')
print("Model trained and saved to modelAverLSTM256128weight.h5")
