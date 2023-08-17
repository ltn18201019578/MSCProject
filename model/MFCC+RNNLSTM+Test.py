from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, precision_score, recall_score,accuracy_score
import numpy as np
import os

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
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\testData4'

# Load the data
features, labels = load_data(directory)

# Load the model
model = load_model('model200.h5')

# Predict the labels for test data
predictions = model.predict(features)

# Convert probabilities into labels
predicted_labels = np.argmax(predictions, axis=1)

# Calculate confusion matrix
conf_mat = confusion_matrix(labels, predicted_labels)

# Calculate precision and recall
precision = precision_score(labels, predicted_labels, average='micro')
recall = recall_score(labels, predicted_labels, average='micro')

# Calculate accuracy
accuracy = accuracy_score(labels, predicted_labels)

# Print results
print("Confusion Matrix:")
print(conf_mat)
print("Precision: ", precision)
print("Recall: ", recall)
print("Accuracy: ", accuracy)