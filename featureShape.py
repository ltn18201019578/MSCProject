import numpy as np
import os

# Your target directory
directory = r"C:\Users\18201\OneDrive\桌面\study\final project\resnetAver"

for filename in os.listdir(directory):
    if filename.endswith(".npy"):
        # Get the full path of the file
        file_path = os.path.join(directory, filename)

        # Load the numpy array
        mfcc = np.load(file_path)

        # Print its shape
        print(f"{filename}: {mfcc.shape}")