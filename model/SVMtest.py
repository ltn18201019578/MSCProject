import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA
import os
import joblib

# Function to load data
def load_data(directory):
    print("Loading data...")
    features = []
    labels = []
    for filename in os.listdir(directory):
        if filename.endswith(".npy"):
            # Load feature vector
            feature = np.load(os.path.join(directory, filename))
            feature = feature.reshape(-1)  # Flatten the array to 1D
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
    print("Data loaded.")
    return features, labels

# The directory where your test data is stored
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\testData4'

# Load the test data
features, labels = load_data(directory)
pca = joblib.load('PCAmodel.pkl')

# Reduce dimensionality using PCA
print("Applying PCA to reduce dimensionality...")
features_pca = pca.transform(features)
print("Dimensionality reduced.")

# Load the trained SVM model
print("Loading the trained SVM model...")
svm_model = joblib.load('SVMmodel.pkl')
print("Model loaded.")

# Evaluate on test set
print("Evaluating on test set...")
y_pred = svm_model.predict(features_pca)
print("Confusion Matrix:")
print(confusion_matrix(labels, y_pred))
print(classification_report(labels, y_pred))
print("Evaluation completed.")
