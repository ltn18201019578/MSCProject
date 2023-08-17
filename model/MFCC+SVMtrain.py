import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
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

# The directory where your data is stored
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\trainData4'

# Load the data
features, labels = load_data(directory)

# Reduce dimensionality using PCA
print("Applying PCA to reduce dimensionality...")
pca = PCA(n_components=200)  # You can adjust the number of components
features_pca = pca.fit_transform(features)
print("Dimensionality reduced.")

# Split the data into training and validation sets
print("Splitting data into training and validation sets...")
X_train, X_val, y_train, y_val = train_test_split(features_pca, labels, test_size=0.2, random_state=42)
print("Data split.")

# Create SVM model with RBF kernel
print("Creating SVM model with RBF kernel...")
svm_model = SVC(kernel='rbf', C=1, gamma='scale')
print("Model created.")

# Train the model
print("Training the model...")
svm_model.fit(X_train, y_train)
print("Training completed.")

# Evaluate on validation set
print("Evaluating on validation set...")
y_pred = svm_model.predict(X_val)
print(classification_report(y_val, y_pred))
print("Evaluation completed.")
# Save the trained PCA model
joblib.dump(pca, 'PCAmodel.pkl')
print("PCA model saved!")
# Save the trained model
print("Saving the trained model...")
joblib.dump(svm_model, 'SVMmodel.pkl')
print("Model saved!")
