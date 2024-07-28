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
# Convert rcois column to lowercase
df['rcois'] = df['rcois'].str.lower()

# Calculate statistics
total_hotspots = len(df)

# Boolean series for each category
openroaming_unsettled_match = df['rcois'].str.contains(
    '5a03ba|4096|5a03ba0000|500b|5a03ba1000|502a|5a03ba0a00|50a7|5a03ba1a00|5014|5a03ba0200|50bd|5a03ba1200|503e|5a03ba0300|50d1|5a03ba1300|5050|50e2|5053|5a03ba0b00|50f0|5a03ba1b00|5054|5a03ba0600|562b|5a03ba1600|5073|5a03ba0100|57d2|5a03ba1100|5a03ba0400|5a03ba0500|5a03ba0800|5a03ba0900',
    na=False
)
openroaming_settled_match = df['rcois'].str.contains(
    'baa2d|500f|baa2d00000|baa2d00100|baa2d01100|baa2d02100|baa2d03100|baa2d04100|baa2d05100|baa2d00500',
    na=False
) & ~openroaming_unsettled_match
google_orion_devices_match = df['rcois'].str.contains('f4f5e8f5f4', na=False)
ironwifi_devices_match = df['rcois'].str.contains('aa146b0000', na=False)
xnet_devices_match = df['ssid'].str.contains('XNET', na=False, case=False)
helium_devices_match = df['ssid'].str.contains('Helium Mobile', na=False, case=False)
wayru_devices_match = df['ssid'].str.contains('Wayru', na=False, case=False)
metablox_devices_match = df['ssid'].str.contains('MetaBlox', na=False, case=False)

# Boolean series for EDUROAM Devices
eduroam_rcois_match = df['rcois'].str.contains('5a03ba0800|1bc50460', na=False)
eduroam_ssid_match = ~eduroam_rcois_match & df['ssid'].str.contains('eduroam®|eduroam', na=False, case=False)
eduroam_devices_match = eduroam_rcois_match | eduroam_ssid_match

# Boolean series for CityRoam devices
cityroam_devices_match = df['ssid'].str.contains('cityroam', na=False, case=False)

# Sum of unique matches
openroaming_unsettled = openroaming_unsettled_match.sum()
openroaming_settled = openroaming_settled_match.sum()
google_orion_devices = google_orion_devices_match.sum()
ironwifi_devices = ironwifi_devices_match.sum()
xnet_devices = xnet_devices_match.sum()
helium_devices = helium_devices_match.sum()
wayru_devices = wayru_devices_match.sum()
metablox_devices = metablox_devices_match.sum()
eduroam_devices = eduroam_devices_match.sum()
cityroam_devices = cityroam_devices_match.sum()

# Boolean series for devices that have been matched
matched_devices = (
    openroaming_unsettled_match |
    openroaming_settled_match |
    google_orion_devices_match |
    ironwifi_devices_match |
    xnet_devices_match |
    helium_devices_match |
    wayru_devices_match |
    metablox_devices_match |
    eduroam_devices_match |
    cityroam_devices_match
)

# Calculate count of unique matched devices
unique_matched_devices = df[matched_devices].drop_duplicates().sort_values(by=['rcois', 'ssid'])

# Calculate count of devices that don't match any of the previous rules
other_devices = total_hotspots - unique_matched_devices.shape[0]

# Print the results
print("Total Hotspots:", total_hotspots)
print("OpenRoaming Unsettled:", openroaming_unsettled)
print("OpenRoaming Settled:", openroaming_settled)
print("Google Orion Devices:", google_orion_devices)
print("IronWiFi Devices:", ironwifi_devices)
print("XNET Devices:", xnet_devices)
print("Helium Devices:", helium_devices)
print("Wayru Devices:", wayru_devices)
print("MetaBlox Devices:", metablox_devices)
print("EDUROAM Devices:", eduroam_devices)
print("CityRoam Devices:", cityroam_devices)
print("Other Devices:", other_devices)

# Get a list of all unique RCOIs, split into individual parts, deduplicate, and sort alphabetically
unique_rcois = df['rcois'].dropna().str.split().explode().unique()
unique_rcois = sorted(set(unique_rcois))
unique_rcois_list = ', '.join(unique_rcois)
print("Unique RCOIs:", unique_rcois_list)

# Calculate most common SSIDs
common_ssids = df['ssid'].value_counts().head(10)

# Create markdown table with descriptions
stats_table = f"""
### OpenRoaming and Hotspot 2.0 Stats Table
| Statistic | Count | Description |
|-----------|-------|-------------|
| Total Hotspot 2.0 APs | {total_hotspots} | Total count of all Hotspot 2.0 access points |
| OpenRoaming Unsettled | {openroaming_unsettled} | Count of devices with RCOI matching any OpenRoaming unsettled RCOI |
| OpenRoaming Settled | {openroaming_settled} | Count of devices with RCOI matching any OpenRoaming settled RCOI |
| EDUROAM Devices | {eduroam_devices} | Count of devices with RCOI containing either '5A03BA0800' or '1BC50460' or with an SSID matching "eduroam" |
| Google Orion Devices | {google_orion_devices} | Count of devices with RCOI containing 'f4f5e8f5f4' |
| IronWiFi Devices | {ironwifi_devices} | Count of devices with RCOI containing 'aa146b0000' |
| XNET Devices | {xnet_devices} | Count of devices with SSID containing 'XNET' |
| Helium Devices | {helium_devices} | Count of devices with SSID containing 'Helium Mobile' |
| Wayru Devices | {wayru_devices} | Count of devices with SSID containing 'Wayru' |
| MetaBlox Devices | {metablox_devices} | Count of devices with SSID containing 'MetaBlox' |
| CityRoam Devices | {cityroam_devices} | Count of devices with SSID containing 'cityroam' |
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
