import matplotlib.pyplot as plt

# Data
accents = ['Northern Accent', 'JAC Accent', 'Southwestern Accent', 'Northwestern Accent']
values = [48480, 9240, 14280, 11880]

# Create the bar plot
plt.figure(figsize=(10, 6))
plt.bar(accents, values, color=['blue', 'green', 'red', 'purple'])
plt.xlabel('Accents')
plt.ylabel('Values')
plt.title('Accents Distribution')
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels
plt.show()
