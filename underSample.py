import os
import shutil
import random

# 创建一个字典来跟踪每个口音的数量
accent_counts = {
    'northern': 0,
    'JAC': 0,
    'southwestern': 0,
    'northwestern': 0,
}

# 设定每个口音的最大数量
max_counts = {
    'northern': 9000,
    'JAC': 9000,
    'southwestern': 9000,
    'northwestern': 9000,
}

# 你的目标文件夹
directory = r'C:\Users\18201\Downloads\ST-CMDS-20170001_1-OS\ST-CMDS-20170001_1-OS'

# 创建一个新的文件夹来存放欠采样的数据
undersampled_directory = r'C:\Users\18201\OneDrive\桌面\study\final project\undersampled_data'
os.makedirs(undersampled_directory, exist_ok=True)

# 遍历目标文件夹中的文件
for filename in os.listdir(directory):
    if filename.endswith(".metadata"):
        # 获取文件的完整路径
        file_path = os.path.join(directory, filename)

        # 读取metadata文件，找到口音类型
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if "BIR" in line:
                    accent = line.split()[1]
                    print(accent)
                    break

        # 如果口音在我们的口音列表中
        if accent in accent_counts:
            # 如果还没有达到最大数量
            if accent_counts[accent] < max_counts[accent]:
                # 移动或复制文件
                shutil.copy(file_path, undersampled_directory)
                shutil.copy(os.path.splitext(file_path)[0] + ".wav", undersampled_directory)

                # 更新数量
                accent_counts[accent] += 1
                print(f"Copied {accent} file {filename} to undersampled directory.")
