import os
import re

# The directory of your metadata files
directory = r"C:\Users\18201\Downloads\ST-CMDS-20170001_1-OS\ST-CMDS-20170001_1-OS"

# Initialize a dictionary to store the count of speakers from each city
city_counts = {}

# Loop through every file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".metadata"):
        try:
            # Try to open the file with utf-8 encoding
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                # Read the file
                content = file.read()
        except UnicodeDecodeError:
            # If an error occurs, try to open the file with gbk encoding
            with open(os.path.join(directory, filename), 'r', encoding='gbk') as file:
                # Read the file
                content = file.read()

        # Find the city using a regular expression
        match = re.search(r'BIR (.*?)\n', content)
        if match:
            # Get the city
            city = match.group(1)
            # If the city is already in the dictionary, increment its count
            if city in city_counts:
                city_counts[city] += 1
            # If the city is not in the dictionary, add it with a count of 1
            else:
                city_counts[city] = 1

# Print the counts for each city
for city, count in city_counts.items():
    print(f"{city}: {count}")