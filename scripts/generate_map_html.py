import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from datetime import datetime

# Get the current working directory
current_path = os.getcwd()

# Define the folder paths
scripts_path = os.path.join(current_path, 'Scripts')
data_path = os.path.join(current_path, 'Data')
output_path = os.path.join(current_path, 'Output')
archive_path = os.path.join(output_path, 'archive')

# Ensure the archive directory exists
os.makedirs(archive_path, exist_ok=True)

# Define the path to the CSV file in the Data folder
file_path = os.path.join(data_path, 'wigle_results.csv')

# Load the CSV file
data = pd.read_csv(file_path)

# Get the current year
current_year = datetime.now().year

# Filter data to include only entries from the current year
data['firsttime'] = pd.to_datetime(data['firsttime'])
data['lasttime'] = pd.to_datetime(data['lasttime'])
data_filtered = data[data['firsttime'].dt.year == current_year]

# Initialize the map centered around the US
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Initialize a MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

# List to store the marker objects for filtering
markers = []

# Add each point to the MarkerCluster and the markers list
for idx, row in data_filtered.iterrows():
    popup_text = (
        f"SSID: {row['ssid']}<br>"
        f"RCOIs: {row['rcois']}<br>"
        f"Coordinates: ({row['trilat']}, {row['trilong']})<br>"
        f"First Seen: {row['firsttime']}<br>"
        f"Last Seen: {row['lasttime']}<br>"
        f"Country: {row['country']}<br>"
        f"Region: {row['region']}<br>"
        f"City: {row['city']}<br>"
        f"Road: {row['road']}<br>"
    )
    
    marker = folium.Marker(
        location=[row['trilat'], row['trilong']],
        popup=popup_text,
        tooltip=row['ssid']
    )
    marker.add_to(marker_cluster)
    markers.append(marker)

# Add the total count display
total_count = len(markers)
total_count_html = f"""
<div style="position: fixed; top: 10px; left: 10px; width: 200px; z-index: 1000; background: white; padding: 10px; border: 1px solid black;">
    Total Nodes: <span id="total-count">{total_count}</span><br>
    Filtered Nodes: <span id="filtered-count">{total_count}</span>
</div>
"""
m.get_root().html.add_child(folium.Element(total_count_html))

# Add custom JavaScript for dynamic filtering and count updating
custom_script = f"""
<script>
    var markers = {markers};

    function updateFilteredCount() {{
        var search_input = document.querySelector('.search-input');
        var filtered_count = 0;
        var searchValue = search_input.value.toLowerCase();
        
        {marker_cluster.get_name()}.clearLayers();
        
        for (var i = 0; i < markers.length; i++) {{
            var ssid = markers[i].options.tooltip.options.content.toLowerCase();
            var popup = markers[i].getPopup().getContent().toLowerCase();
            
            if (ssid.includes(searchValue) || popup.includes(searchValue)) {{
                {marker_cluster.get_name()}.addLayer(markers[i]);
                filtered_count++;
            }}
        }}
        
        document.getElementById('filtered-count').innerText = filtered_count;
    }}

    document.querySelector('.search-input').addEventListener('input', updateFilteredCount);
</script>
"""
m.get_root().html.add_child(folium.Element(custom_script))

# Save the map to an HTML file in the Output folder
map_file_path = os.path.join(output_path, 'wigle_map.html')
archive_file_path = os.path.join(archive_path, f'wigle_map_{current_year}.html')

m.save(map_file_path)
m.save(archive_file_path)

print(f"Map has been saved to {map_file_path} and archived to {archive_file_path}")
