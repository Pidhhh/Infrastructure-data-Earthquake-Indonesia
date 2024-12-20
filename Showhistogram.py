import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the data (adjust the file path accordingly)
file_path = 'Change' # Adjust the file path accordingly
print('Change the file path to the dataset') # Delete this line if you have changed the file path

data = pd.read_csv(file_path)

# Plot histogram
plt.figure(figsize=(10, 6))
sns.histplot(data['Magnitude'], bins=20, kde=True, color='blue')
plt.title('Distribusi Magnitudo Gempa', fontsize=14)
plt.xlabel('Magnitude', fontsize=12)
plt.ylabel('Frekuensi', fontsize=12)
plt.grid(alpha=0.5)
plt.show()
