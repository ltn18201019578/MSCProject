import os

# 你的口音和城市映射
accent_mapping = {
    "northern accent": ["北京", "山东", "河北", "天津", "烟台", "石家庄", "内蒙", "内蒙古", "河南", "吉林", "黑龙江", "辽宁", "辽阳", "东北", "鞍山", "大连", "葫芦岛"],
    "southwestern accent": ["四川", "重庆", "云南", "西藏", "贵州", "湖北"],
    "northwestern accent": ["陕西", "甘肃", "青海", "宁夏", "新疆"],
    "JAC accent": ["浙江", "上海", "苏州", "江苏", "安徽"],
    "South China  ": ["广东", "福建", "海南", "广西"],
    "Gan accent": ["江西", "湖南"],
    "Jin accent": ["山西"]
}
directory = 'C:/Users/18201/Downloads/ST-CMDS-20170001_1-OS/ST-CMDS-20170001_1-OS'

# 从口音映射创建城市到口音的映射
city_to_accent = {city: accent for accent, cities in accent_mapping.items() for city in cities}

for filename in os.listdir(directory):
    if filename.endswith(".metadata"):
        # 获取文件的完整路径
        file_path = os.path.join(directory, filename)

        try:
            # 尝试用utf-8编码打开文件
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            # 如果报错，则尝试用gbk编码打开文件
            with open(file_path, 'r', encoding='gbk') as file:
                lines = file.readlines()

        # 对每一行进行处理
        for i in range(len(lines)):
            # 如果城市名在我们的映射中，我们就更新它
            # 注意，我们现在需要把 "BIR " 去掉才能得到城市名
            line = lines[i]
            if line.startswith('BIR'):
                city = line.split(' ')[1].strip()
                if city in city_to_accent:
                    lines[i] = "BIR " + city_to_accent[city] + '\n'

        # 将更新后的数据写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)