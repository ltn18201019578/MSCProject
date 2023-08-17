import os
import re
from collections import defaultdict

def extract_city(metadata_file):
    try:
        with open(metadata_file, 'r', encoding='UTF-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(metadata_file, 'r', encoding='gbk') as f:
            content = f.read()
    match = re.search(r'BIR (.*?)\n', content)
    if match:
        print(match)
        return match.group(1)
    else:
        return None

# 你的.metadata文件所在的目录
directory = r'C:\Users\18201\OneDrive\桌面\study\final project\trainData4'

city_dict = defaultdict(int) # 初始化一个默认字典，如果访问不存在的键，返回默认值0

for filename in os.listdir(directory):
    if filename.endswith('.metadata'):
        city = extract_city(os.path.join(directory, filename))
        if city:
            print(city)
            city_dict[city] += 1

for city, count in city_dict.items():

    print(f'City: {city}, Count: {count}')