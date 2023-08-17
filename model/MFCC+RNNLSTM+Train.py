import time

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os
import numpy as np

# Define model architecture
from tensorflow.keras.layers import Dropout
from tensorflow.keras.regularizers import l2

def create_model():
    model = Sequential()
    model.add(LSTM(256, return_sequences=True, input_shape=(13, 164)))  # LSTM layer
    # model.add(Dropout(0.5))
    model.add(LSTM(128))  # LSTM layer
    # model.add(Dropout(0.5))
    model.add(Dense(64, activation ='relu'))  # Dense layer
    model.add(Dense(4, activation ='softmax'))  # Output layer
    # Compile the model
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Load data
def load_data(directory):
    features = []
    labels = []
    for filename in os.listdir(directory):
        if filename.endswith(".npy"):
            # Load feature vector
            feature = np.load(os.path.join(directory, filename))
            features.append(feature)
            # Load corresponding label
            metadata_file = os.path.join(directory, filename.replace('.npy', '.metadata'))
            try:
                with open(metadata_file, 'r', encoding='UTF-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(metadata_file, 'r', encoding='gbk') as f:
                    content = f.read()
            accent_line = next(line for line in content.split('\n') if line.startswith('BIR'))
            label = int(accent_line.split(' ')[1])
            labels.append(label)
    # Convert to numpy arrays
    features = np.array(features)
    labels = np.array(labels)
    return features, labels

# The directory where your data is stored
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\trainData4'

# Load the data
features, labels = load_data(directory)

# Create the model
model = create_model()
start_time = time.time()  # 记录开始时间

# Train the model
model.fit(features, labels, epochs=200, validation_split=0.2)
end_time = time.time()  # 记录结束时间
print("Training time: {:.2f} seconds".format(end_time - start_time))

model.save('model200.h5')