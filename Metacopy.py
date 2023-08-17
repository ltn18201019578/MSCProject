import shutil
import os

input_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\last\test'
output_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\last\testSplit'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for filename in os.listdir(input_directory):
    if filename.endswith('.metadata'):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, filename)
        shutil.copy(input_file_path, output_file_path)
        print(f"Copied: {filename}")