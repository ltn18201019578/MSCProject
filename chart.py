import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties

# File path
file_path = r"C:\Users\18201\OneDrive\桌面\1.txt"

# Read the file content
data = pd.read_csv(file_path, sep=":", names=["地区", "个数"], encoding='utf-8')

# Set Chinese font
font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=10)

# Plot the bar chart
fig, ax = plt.subplots(figsize=(18, 6))
bars = ax.bar(range(len(data["个数"])), data["个数"])
plt.xlabel("地区索引", fontproperties=font)
plt.ylabel("个数", fontproperties=font)
plt.title("各地区个数统计", fontproperties=font)

# Prepare cell text for the table
region_names = [name for name in data["地区"]]
cell_text = [region_names[i:i+10] + [''] * (10 - len(region_names[i:i+10])) for i in range(0, len(region_names), 10)]

# Add a table with the region names
table = plt.table(cellText=cell_text, loc='right', colWidths=[0.1] * 10)

# Adjust layout
table.auto_set_font_size(False)
table.set_fontsize(1)
table.scale(1, 1.5)  # Adjust the row height of the table
plt.tight_layout()
plt.subplots_adjust(right=0.5)  # Adjust plot to make room for the table

# Set Chinese font for the table
for key, cell in table.get_celld().items():
    cell.set_text_props(fontproperties=font)

plt.show()
