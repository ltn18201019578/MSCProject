import os
import time

import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, GlobalAveragePooling2D, Reshape
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

def create_resnet_lstm(input_shape, num_classes):
    print("Creating ResNet-LSTM model...")
    base_model = ResNet50(include_top=False, weights='imagenet', input_shape=input_shape)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Reshape((1, -1))(x)
    x = LSTM(256, return_sequences=True)(x)
    x = LSTM(128)(x)
    x = Dense(64, activation='relu')(x)
    outputs = Dense(num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# The directory where your spectrogram files are stored
spectrogram_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\spectrograms'
audio_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\trainData4'

# Load the data
spectrograms, labels = load_data(spectrogram_directory,audio_directory)

# Create the ResNet-LSTM model
input_shape = (spectrograms.shape[1], spectrograms.shape[2], spectrograms.shape[3])
num_classes = 4  # Number of classes for classification
model = create_resnet_lstm(input_shape, num_classes)

# Train the model
print("Training model...")
start_time = time.time()  # 记录开始时间
model.fit(spectrograms, labels, epochs=40, validation_split=0.2)
end_time = time.time()  # 记录结束时间
print("Training time: {:.2f} seconds".format(end_time - start_time))
model.save('AverLST40.h5')
print("Model trained and saved to AverLST20.h5")
