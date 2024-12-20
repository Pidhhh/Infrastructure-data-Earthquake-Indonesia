import pandas as pd
import matplotlib.pyplot as plt     # Import the Matplotlib Pyplot module for plotting
import cartopy.crs as ccrs # Import the Cartopy Coordinate Reference System (CRS)
import cartopy.feature as cfeature  # Import the Cartopy Features

# Load data 
file_path = "Earthquake-Data/indonesia_earthquake_data_20241205130928.csv"
data = pd.read_csv(file_path)

# Plot setup
plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([94, 141, -11, 6], crs=ccrs.PlateCarree())  # Batas Indonesia

# Add map features
ax.add_feature(cfeature.LAND, color='lightgray')  # Warna daratan
ax.add_feature(cfeature.OCEAN, color='aqua')      # Warna laut
ax.add_feature(cfeature.COASTLINE)               # Garis pantai
ax.add_feature(cfeature.BORDERS, linestyle=':')  # Garis batas negara

# Scatter plot untuk gempa
scatter = plt.scatter(data['Longitude'], data['Latitude'], 
                       c=data['Magnitude'], cmap='viridis', s=50, alpha=0.7, transform=ccrs.PlateCarree())
plt.colorbar(scatter, label='Magnitude')

# Title and labels
plt.title('Sebaran Lokasi Gempa di Indonesia', fontsize=14)
plt.show()
