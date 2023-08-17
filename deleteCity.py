import os

# Your target directory
directory = r'C:\Users\18201\Downloads\ST-CMDS-20170001_1-OS\ST-CMDS-20170001_1-OS'

for filename in os.listdir(directory):
    if filename.endswith(".metadata"):
        # Get the full path of the file
        file_path = os.path.join(directory, filename)

        try:
            # Try to open the file with utf-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.readlines()
        except UnicodeDecodeError:
            # If an error occurs, try to open the file with gbk encoding
            with open(file_path, 'r', encoding='gbk') as file:
                data = file.readlines()
        for i, line in enumerate(data):
            if 'BIR 汉' in line:  # 现在检查的是'BIR 北京'是否在行中
                os.remove(file_path)
                wav_file_path = os.path.splitext(file_path)[0] + ".wav"
                if os.path.exists(wav_file_path):
                    os.remove(wav_file_path)
