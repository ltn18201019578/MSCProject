import os

# Your target directory
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\last\testSplit'

# The mapping from accent to integer
accent_to_int = {
    "northern": 0,
    "JAC": 1,
    "southwestern": 2,
    "northwestern": 3,
}
# accent_to_int = {
#     "男": 0,
#     "女": 1,
# }


for filename in os.listdir(directory):
    if filename.endswith(".metadata"):
        # Get the full path of the file
        file_path = os.path.join(directory, filename)
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Find the line that contains the accent and replace the accent with its corresponding integer
        for i, line in enumerate(lines):
            if line.startswith('BIR'):
                accent = line.split(' ')[1]
                if accent in accent_to_int:
                    print(accent_to_int)

                    lines[i] = line.replace(accent, str(accent_to_int[accent]))
        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
