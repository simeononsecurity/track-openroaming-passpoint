import os
import pandas as pd

# Get the current working directory
current_path = os.getcwd()

# Define the folder paths
scripts_path = os.path.join(current_path, 'scripts')
data_path = os.path.join(current_path, 'data')
output_path = os.path.join(current_path, 'output')

# Define the path to the CSV file in the Data folder
csv_path = os.path.join(data_path, 'wigle_results.csv')

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_path)

# Convert time columns to datetime for comparison
df['firsttime'] = pd.to_datetime(df['firsttime'])
df['lasttime'] = pd.to_datetime(df['lasttime'])
df['lastupdt'] = pd.to_datetime(df['lastupdt'])

# Sort by geocoordinates, SSID, MAC address, and then by 'lastupdt' to keep the latest entry
df = df.sort_values(by=['trilat', 'trilong', 'ssid', 'netid', 'lastupdt'], ascending=[True, True, True, True, False])

# Drop duplicates by geocoordinates with the same SSID or MAC address, keeping only the latest
df_unique = df.drop_duplicates(subset=['trilat', 'trilong', 'ssid', 'netid'], keep='first')

# Filter out rows with duplicate SSIDs or MAC addresses but keep them if other columns differ
# Create a new DataFrame to store filtered results
filtered_df = pd.DataFrame()

# Group by SSID and MAC address and apply filtering
for _, group in df_unique.groupby(['ssid', 'netid']):
    if group.duplicated(subset=['trilat', 'trilong']).any():
        # If duplicates are found based on geocoordinates, keep the latest entry
        latest_entry = group.sort_values(by='lastupdt', ascending=False).iloc[0]
        filtered_df = filtered_df._append(latest_entry)
    else:
        # If no duplicates based on geocoordinates, keep all entries
        filtered_df = filtered_df._append(group)

# Reset the index for the final DataFrame
filtered_df.reset_index(drop=True, inplace=True)

# Save the filtered DataFrame to a new CSV file in the Data folder
filtered_csv_path = os.path.join(data_path, 'wigle_results_filtered.csv')
filtered_df.to_csv(filtered_csv_path, index=False)

print(f"Filtered data saved to {filtered_csv_path}")