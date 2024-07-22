import os
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm

# Define the folder paths
current_path = os.getcwd()
data_path = os.path.join(current_path, 'data')

# Ensure directories exist
os.makedirs(data_path, exist_ok=True)

# Define the path to the CSV file in the Data folder
csv_file = os.path.join(data_path, 'wigle_results.csv')
output_file = os.path.join(data_path, 'classified_wigle_results.csv')

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Convert SSID column to string and handle NaN values
df['ssid'] = df['ssid'].astype(str).fillna('')

# SSID heuristics
residential_ssids = ["Home", "NETGEAR", "Linksys", "ATT", "Comcast", "Xfinity"]
business_ssids = ["Guest", "Office", "Corp", "WiFi", "Business", "Cafe", "Store", "Shop"]
public_ssids = ["FreeWiFi", "Public", "Library", "Airport", "Hotel", "City"]

def classify_ssid(ssid):
    for res_ssid in residential_ssids:
        if res_ssid.lower() in ssid.lower():
            return "Residential"
    for bus_ssid in business_ssids:
        if bus_ssid.lower() in ssid.lower():
            return "Business"
    for pub_ssid in public_ssids:
        if pub_ssid.lower() in ssid.lower():
            return "Public"
    return "Unknown"

# Add a new column for classification
df['location_type'] = df['ssid'].apply(classify_ssid)

# Set up the geolocator
geolocator = Nominatim(user_agent="track-openroaming-passpoint")
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1, return_value_on_exception={})

# Function for reverse geocoding using geopy
def reverse_geocode(lat, lon):
    try:
        location = geocode((lat, lon), exactly_one=True)
        return location.raw['address'] if location else {}
    except Exception as e:
        print(f"Reverse geocoding failed for ({lat}, {lon}): {e}")
        return {}

# Add a new column for reverse geocoded address
address_components = ['road', 'suburb', 'city', 'town', 'village', 'county', 'state', 'country']
for component in address_components:
    df[component] = ""

# Perform reverse geocoding and fill address components
for idx, row in tqdm(df.iterrows(), total=df.shape[0], desc="Reverse Geocoding"):
    if row['location_type'] == "Unknown":
        address = reverse_geocode(row['trilat'], row['trilong'])
        for component in address_components:
            df.at[idx, component] = address.get(component, "")

# Save the classified DataFrame to a new CSV file
df.to_csv(output_file, index=False)
print(f"Classified data has been saved to {output_file}")
