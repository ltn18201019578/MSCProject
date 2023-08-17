import os

def extract_audio_filename(filepath):
    try:
        with open(filepath, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='gbk') as f:
            lines = f.readlines()
    for i, line in enumerate(lines):
        if 'BIR 上海' in line:  # 现在检查的是'BIR 北京'是否在行中
            return os.path.basename(filepath)  # 返回当前.metadata文件名
    return None

directory = 'C:/Users/18201/Downloads/ST-CMDS-20170001_1-OS/ST-CMDS-20170001_1-OS'  # 替换成你的.metadata文件所在目录

for filename in os.listdir(directory):
    if filename.endswith('.metadata'):
        metadata_filename = extract_audio_filename(os.path.join(directory, filename))
        if metadata_filename:
            print(metadata_filename)