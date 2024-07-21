import os
import pandas as pd

# Define the folder paths
current_path = os.getcwd()
data_path = os.path.join(current_path, 'data')
readme_path = os.path.join(current_path, 'README.md')

# Define the path to the CSV file in the Data folder
csv_file = os.path.join(data_path, 'wigle_results.csv')

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Calculate statistics
total_hotspots = len(df)
openroaming_unsettled = df['rcois'].str.contains('5a03ba', na=False).sum()
openroaming_settled = df['rcois'].str.contains('baa2d', na=False) & ~df['rcois'].str.contains('5a03ba', na=False)
openroaming_settled = openroaming_settled.sum()
google_orion_devices = df['rcois'].str.contains('f4f5e8f5f4', na=False).sum()
xnet_devices = df['ssid'].str.contains('XNET', na=False).sum()
helium_devices = df['ssid'].str.contains('Helium', na=False).sum()

# Calculate count of devices that don't match any of the previous rules
other_devices = total_hotspots - (
    openroaming_unsettled + openroaming_settled + google_orion_devices + xnet_devices + helium_devices
)

# Calculate most common SSIDs
common_ssids = df['ssid'].value_counts().head(10)

# Create markdown table with descriptions
stats_table = f"""
| Statistic | Count | Description |
|-----------|-------|-------------|
| Total Hotspot 2.0 APs | {total_hotspots} | Total count of all Hotspot 2.0 access points |
| OpenRoaming Unsettled | {openroaming_unsettled} | Count of devices with RCOI containing '5a03ba' |
| OpenRoaming Settled | {openroaming_settled} | Count of devices with RCOI containing 'baa2d' but not '5a03ba' |
| Google Orion Devices | {google_orion_devices} | Count of devices with RCOI containing 'f4f5e8f5f4' |
| XNET Devices | {xnet_devices} | Count of devices with SSID containing 'XNET' |
| Helium Devices | {helium_devices} | Count of devices with SSID containing 'HELIUM' |
| Other Devices | {other_devices} | Count of devices that do not match any of the above categories |
"""

# Create markdown table for most common SSIDs
ssids_table = """
### Most Common RCOI Enabled SSIDs
| SSID | Count |
|------|-------|
"""
for ssid, count in common_ssids.items():
    ssids_table += f"| {ssid} | {count} |\n"

# Read the README file
with open(readme_path, 'r') as f:
    readme_content = f.read()

# Ensure the markers are present in the README
if '<!-- STATS START -->' in readme_content and '<!-- STATS END -->' in readme_content:
    before_stats, after_stats = readme_content.split('<!-- STATS START -->')[0], readme_content.split('<!-- STATS END -->')[1]
    new_readme_content = before_stats + '<!-- STATS START -->\n' + stats_table + '\n' + ssids_table + '\n<!-- STATS END -->' + after_stats

    # Write the new content back to the README file
    with open(readme_path, 'w') as f:
        f.write(new_readme_content)

    print("README.md has been updated with new statistics.")
else:
    print("Error: Markers <!-- STATS START --> and <!-- STATS END --> not found in README.md.")
