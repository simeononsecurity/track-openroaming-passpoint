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

# Create a unique identifier for each device based on all columns
df['device_id'] = df.apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

# Calculate statistics
total_hotspots = len(df)

# Split the RCOIs into separate rows
rcois_expanded = df['rcois'].str.split(expand=True).stack().reset_index(level=1, drop=True)
rcois_expanded.name = 'rcoi'

# Create a DataFrame from the expanded RCOIs
rcoi_df = df.join(rcois_expanded).drop(columns=['rcois'])

# Boolean series for each category
openroaming_unsettled_match = rcoi_df['rcoi'].str.contains(
    '5a03ba|4096|5a03ba0000|500b|5a03ba1000|502a|5a03ba0a00|50a7|5a03ba1a00|5014|5a03ba0200|50bd|5a03ba1200|503e|5a03ba0300|50d1|5a03ba1300|5050|50e2|5053|5a03ba0b00|50f0|5a03ba1b00|5054|5a03ba0600|562b|5a03ba1600|5073|5a03ba0100|57d2|5a03ba1100|5a03ba0400|5a03ba0500|5a03ba0800|5a03ba0900',
    na=False
)
openroaming_settled_match = rcoi_df['rcoi'].str.contains(
    'baa2d|500f|baa2d00000|baa2d00100|baa2d01100|baa2d02100|baa2d03100|baa2d04100|baa2d05100|baa2d00500|baa2d0|baa2d06000',
    na=False
) & ~openroaming_unsettled_match
google_orion_devices_match = rcoi_df['rcoi'].str.contains('f4f5e8f5f4', na=False)
ironwifi_devices_match = rcoi_df['rcoi'].str.contains('aa146b0000', na=False)
xnet_devices_match = rcoi_df['ssid'].str.contains('XNET', na=False, case=False)
helium_devices_match = rcoi_df['ssid'].str.contains('Helium Mobile', na=False, case=False)
wayru_devices_match = rcoi_df['ssid'].str.contains('Wayru', na=False, case=False)
metablox_devices_match = rcoi_df['ssid'].str.contains('MetaBlox', na=False, case=False)

# Boolean series for EDUROAM Devices
eduroam_rcois_match = rcoi_df['rcoi'].str.contains('5a03ba0800|1bc50460', na=False)
eduroam_ssid_match = ~eduroam_rcois_match & rcoi_df['ssid'].str.contains('eduroam®|eduroam', na=False, case=False)
eduroam_devices_match = eduroam_rcois_match | eduroam_ssid_match

# Boolean series for CityRoam devices
cityroam_devices_match = rcoi_df['ssid'].str.contains('cityroam', na=False, case=False)

# Function to count unique devices for each match
def count_unique_devices(df, match):
    unique_devices = df[match].drop_duplicates(subset=['device_id']).shape[0]
    return unique_devices

# Count unique devices for each category
openroaming_unsettled = count_unique_devices(rcoi_df, openroaming_unsettled_match)
openroaming_settled = count_unique_devices(rcoi_df, openroaming_settled_match)
google_orion_devices = count_unique_devices(rcoi_df, google_orion_devices_match)
ironwifi_devices = count_unique_devices(rcoi_df, ironwifi_devices_match)
xnet_devices = count_unique_devices(rcoi_df, xnet_devices_match)
helium_devices = count_unique_devices(rcoi_df, helium_devices_match)
wayru_devices = count_unique_devices(rcoi_df, wayru_devices_match)
metablox_devices = count_unique_devices(rcoi_df, metablox_devices_match)
eduroam_devices = count_unique_devices(rcoi_df, eduroam_devices_match)
cityroam_devices = count_unique_devices(rcoi_df, cityroam_devices_match)

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

# Calculate count of devices that don't match any of the previous rules
other_devices = rcoi_df[~matched_devices].drop_duplicates(subset=['device_id']).shape[0]

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

# Calculate counts for each unique RCOI
rcoi_counts = rcoi_df['rcoi'].value_counts()

# Get a list of all unique RCOIs, deduplicate, and sort alphabetically
unique_rcois = sorted(set(rcoi_counts.index))

# Create a dictionary for RCOI definitions
rcoi_definitions = {
    '1bc50460': 'Eduroam Legacy',
    '310280': 'ATT Offload ?',
    '310410': 'ATT Offload ?',
    '313100': 'ATT Offload ?',
    '3af521': 'SingleDigits Testing RCOI',
    '4096': 'OpenRoaming Unsettled Legacy / Samsung OneUI',
    '5a03ba': 'OpenRoaming Unsettled',
    '5a03ba0000': 'OpenRoaming Unsettled (All)',
    '5a03ba0100': 'OpenRoaming Unsettled (SP free Bronze Qos)',
    '5a03ba0200': 'OpenRoaming Unsettled (Cloud or Social ID)',
    '5a03ba0300': 'OpenRoaming Unsettled (Enterprise Employee ID)',
    '5a03ba0400': 'OpenRoaming Unsettled (Government ID free)',
    '5a03ba0500': 'OpenRoaming Unsettled (Automotive ID free)',
    '5a03ba0600': 'OpenRoaming Unsettled (Loyalty Hospitality ID)',
    '5a03ba0800': 'OpenRoaming Unsettled (Education or Research ID free)',
    '5a03ba0900': 'OpenRoaming Unsettled (Cable ID free)',
    '5a03ba0a00': 'OpenRoaming Unsettled (Device manufacturer all ID)',
    '5a03ba0b00': 'OpenRoaming Unsettled (Loyalty Retail ID)',
    '5a03ba1000': 'OpenRoaming Unsettled (All with real ID)',
    '5a03ba1100': 'OpenRoaming Unsettled (SP free Bronze Qos Real ID)',
    '5a03ba1200': 'OpenRoaming Unsettled (Cloud or Social real ID)',
    '5a03ba1300': 'OpenRoaming Unsettled (Enterprise Employee real ID)',
    '5a03ba1600': 'OpenRoaming Unsettled (Loyalty Hospitality real ID)',
    '5a03ba1a00': 'OpenRoaming Unsettled (Device manufacturer real ID only)',
    '5a03ba1b00': 'OpenRoaming Unsettled (Loyalty Retail real ID)',
    '00500b': 'OpenRoaming Unsettled Legacy (All with real ID)',
    '00500f': 'OpenRoaming Settled Legacy (All paid members)',
    '005014': 'OpenRoaming Unsettled Legacy (Cloud or Social ID)',
    '00502a': 'OpenRoaming Unsettled Legacy (Device manufacturer all ID)',
    '00503e': 'OpenRoaming Unsettled Legacy (Enterprise Employee ID)',
    '005050': 'OpenRoaming Unsettled Legacy (Enterprise Customer ID)',
    '005053': 'OpenRoaming Unsettled Legacy (Loyalty Retail ID)',
    '005054': 'OpenRoaming Unsettled Legacy Legacy (Loyalty Hospitality ID)',
    '005073': 'OpenRoaming Unsettled Legacy Legacy (SP free Bronze Qos)',
    '0050a7': 'OpenRoaming Unsettled Legacy (Device manufacturer real ID only)',
    '0050bd': 'OpenRoaming Unsettled Legacy (Cloud or Social real ID)',
    '0050d1': 'OpenRoaming Unsettled Legacy (Enterprise Employee real ID)',
    '0050e2': 'OpenRoaming Unsettled Legacy (Enterprise Customer real ID)',
    '0050f0': 'OpenRoaming Unsettled Legacy (Loyalty Retail real ID)',
    '00562b': 'OpenRoaming Unsettled Legacy Legacy (Loyalty Hospitality real ID)',
    '0057d2': 'OpenRoaming Unsettled Legacy Legacy (SP free Bronze Qos Real ID)',
    'baa2d': 'OpenRoaming Settled',
    'baa2d00000': 'OpenRoaming Settled (All paid members)',
    'baa2d00100': 'OpenRoaming Settled (SP paid Bronze QoS)',
    'baa2d01100': 'OpenRoaming Settled (SP paid Bronze QoS real ID)',
    'baa2d02100': 'OpenRoaming Settled (SP paid Silver QoS)',
    'baa2d03100': 'OpenRoaming Settled (SP paid Silver QoS real ID)',
    'baa2d04100': 'OpenRoaming Settled (SP paid Gold QoS)',
    'baa2d05100': 'OpenRoaming Settled (SP paid Gold QoS real ID)',
    'baa2d00500': 'OpenRoaming Settled (Automotive Paid)',
    'baa2d0': 'OpenRoaming Settled',
    'baa2d06000': 'OpenRoaming Settled',
    'f4f5e8f5f4': 'Google Orion Devices',
    'aa146b0000': 'IronWiFi Devices'
}

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

# Create markdown table for unique RCOIs and their definitions with counts
rcoi_table = "### Unique RCOIs\n| RCOI | Definition | Count |\n|------|------------|-------|\n"
for rcoi in unique_rcois:
    definition = rcoi_definitions.get(rcoi, "Unknown")
    count = rcoi_counts.get(rcoi, 0)
    rcoi_table += f"| {rcoi} | {definition} | {count} |\n"

# Read the README file
with open(readme_path, 'r') as f:
    readme_content = f.read()

# Ensure the markers are present in the README
if '<!-- STATS START -->' in readme_content and '<!-- STATS END -->' in readme_content:
    before_stats, after_stats = readme_content.split('<!-- STATS START -->')[0], readme_content.split('<!-- STATS END -->')[1]
    new_readme_content = before_stats + '<!-- STATS START -->\n' + stats_table + '\n' + ssids_table + '\n' + rcoi_table + '\n<!-- STATS END -->' + after_stats

    # Write the new content back to the README file
    with open(readme_path, 'w') as f:
        f.write(new_readme_content)

    print("README.md has been updated with new statistics.")
else:
    print("Error: Markers <!-- STATS START --> and <!-- STATS END --> not found in README.md.")
