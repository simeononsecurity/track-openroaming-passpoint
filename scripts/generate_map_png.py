import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime

# Get the current working directory
current_path = os.getcwd()

# Define the folder paths
scripts_path = os.path.join(current_path, 'scripts')
data_path = os.path.join(current_path, 'data')
output_path = os.path.join(current_path, 'output')
archive_path = os.path.join(output_path, 'archive')

# Ensure the archive directory exists
os.makedirs(archive_path, exist_ok=True)

# Define the path to the CSV file in the Data folder
csv_path = os.path.join(data_path, 'wigle_results.csv')

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_path)

# Get the current year
current_year = datetime.now().year

# Filter data to include only entries from the current year
df['firsttime'] = pd.to_datetime(df['firsttime'])
df['lasttime'] = pd.to_datetime(df['lasttime'])
df_filtered = df[df['firsttime'].dt.year == current_year]

# Initialize the map
plt.figure(figsize=(20, 10))
m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')

# Draw coastlines and countries
m.drawcoastlines()
m.drawcountries()

# Plot each point on the map
for index, row in df_filtered.iterrows():
    x, y = m(row['trilong'], row['trilat'])
    m.plot(x, y, 'bo', markersize=2, alpha=0.5)  # Blue dot for each point

# Add title
plt.title('Global WiFi Map for All SSIDs (Current Year)')

# Save and show the plot
output_file_path = os.path.join(output_path, 'global_wifi_map.png')
archive_file_path = os.path.join(archive_path, f'global_wifi_map_{current_year}.png')

plt.savefig(output_file_path, dpi=300)
plt.savefig(archive_file_path, dpi=300)
#plt.show()

print(f"Map has been saved to {output_file_path} and archived to {archive_file_path}")
