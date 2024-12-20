import matplotlib.pyplot as plt
import pandas as pd

# Load the data (adjust the file path accordingly)
file_path = 'Change' # Adjust the file path accordingly
print('Change the file path to the dataset') # Delete this line if you have changed the file path

data = pd.read_csv(file_path)

# Check if the necessary columns exist in the dataset
print(data.columns)

# Scatter plot of magnitude vs depth
plt.figure(figsize=(12, 8))
plt.scatter(data['Depth (km)'], data['Magnitude'], alpha=0.6, color='red')
plt.title('Korelasi Kedalaman dan Magnitudo Gempa', fontsize=14)
plt.xlabel('Depth (km)', fontsize=12)
plt.ylabel('Magnitude', fontsize=12)
plt.grid(alpha=0.5)
plt.show()
