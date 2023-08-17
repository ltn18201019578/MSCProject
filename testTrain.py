import os
import numpy as np
import shutil

# Your source directory
source_dir = r'C:\Users\18201\OneDrive\桌面\study\final project\undersampled_data'

# Define the train and test directory
train_dir = r'C:\Users\18201\OneDrive\桌面\study\final project\last\train'
test_dir = r'C:\Users\18201\OneDrive\桌面\study\final project\last\test' # modify this path to where you want to store the test data

# Make sure the train and test directories exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Get all the files
all_files = [f for f in os.listdir(source_dir) if f.endswith('.wav') or f.endswith('.metadata')]

# Create lists to hold the base filenames
base_filenames = []

# Loop over all the files
for f in all_files:
    # Get the base filename (without extension)
    base_filename = os.path.splitext(f)[0]
    # Append it to the list if it's not already in there
    if base_filename not in base_filenames:
        base_filenames.append(base_filename)

# Shuffle the list
np.random.shuffle(base_filenames)

# Determine the number of files for training (80%)
num_train = int(0.8 * len(base_filenames))

# Split the files into training and test sets
train_files = base_filenames[:num_train]
test_files = base_filenames[num_train:]

# Now move the files to the appropriate directories
for file in train_files:
    # Move the wav file
    shutil.move(os.path.join(source_dir, file + '.wav'), train_dir)
    # Move the metadata file
    shutil.move(os.path.join(source_dir, file + '.metadata'), train_dir)

for file in test_files:
    # Move the wav file
    shutil.move(os.path.join(source_dir, file + '.wav'), test_dir)
    # Move the metadata file
    shutil.move(os.path.join(source_dir, file + '.metadata'), test_dir)
