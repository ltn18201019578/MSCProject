import os
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# The directory where your test ResNet features are stored
test_resnet_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\resnetAverTest'

# The directory where your test labels are stored
test_audio_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\testData4'

# Function to load data
def load_data(resnet_directory, audio_directory):
    features = []
    labels = []
    print(f"Loading data from {resnet_directory}...")
    for filename in os.listdir(resnet_directory):
        if filename.endswith(".npy"):
            file_path = os.path.join(resnet_directory, filename)
            feature = np.load(file_path)
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

# Load the test features and labels
print("Loading test features and labels...")
test_features, test_labels = load_data(test_resnet_directory, test_audio_directory)

# Load the trained model
print("Loading the trained model...")
model = load_model('modelAverLSTM256128200.h5')

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
