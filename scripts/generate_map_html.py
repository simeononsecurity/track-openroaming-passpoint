import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from datetime import datetime
import json

# Get the current working directory
current_path = os.getcwd()

# Define the folder paths
data_path = os.path.join(current_path, 'data')
output_path = os.path.join(current_path, 'output')
docs_path = os.path.join(current_path, 'docs')
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
data_filtered = data[data['firsttime'].dt.year == current_year].reset_index(drop=True)

# Define categories
categories = {
    "OpenRoaming Unsettled": data_filtered['rcois'].str.contains(
        '5a03ba|4096|5a03ba0000|500b|5a03ba1000|502a|5a03ba0a00|50a7|5a03ba1a00|5014|5a03ba0200|50bd|5a03ba1200|503e|5a03ba0300|50d1|5a03ba1300|5050|50e2|5053|5a03ba0b00|50f0|5a03ba1b00|5054|5a03ba0600|562b|5a03ba1600|5073|5a03ba0100|57d2|5a03ba1100|5a03ba0400|5a03ba0500|5a03ba0800|5a03ba0900', na=False),
    "OpenRoaming Settled": data_filtered['rcois'].str.contains(
        'baa2d|500f|baa2d00000|baa2d00100|baa2d01100|baa2d02100|baa2d03100|baa2d04100|baa2d05100|baa2d00500', na=False) & ~data_filtered['rcois'].str.contains(
        '5a03ba|4096|5a03ba0000|500b|5a03ba1000|502a|5a03ba0a00|50a7|5a03ba1a00|5014|5a03ba0200|50bd|5a03ba1200|503e|5a03ba0300|50d1|5a03ba1300|5050|50e2|5053|5a03ba0b00|50f0|5a03ba1b00|5054|5a03ba0600|562b|5a03ba1600|5073|5a03ba0100|57d2|5a03ba1100|5a03ba0400|5a03ba0500|5a03ba0800|5a03ba0900', na=False),
    "Google Orion Devices": data_filtered['rcois'].str.contains('f4f5e8f5f4', na=False),
    "IronWiFi Devices": data_filtered['rcois'].str.contains('aa146b0000', na=False),
    "XNET Devices": data_filtered['ssid'].str.contains('XNET', na=False, case=False),
    "Helium Devices": data_filtered['ssid'].str.contains('Helium Mobile', na=False, case=False),
    "Wayru Devices": data_filtered['ssid'].str.contains('Wayru', na=False, case=False),
    "MetaBlox Devices": data_filtered['ssid'].str.contains('MetaBlox', na=False, case=False),
    "EDUROAM Devices": data_filtered['rcois'].str.contains('5a03ba0800|1bc50460', na=False) | data_filtered['ssid'].str.contains('eduroam®|eduroam', na=False, case=False),
    "CityRoam Devices": data_filtered['ssid'].str.contains('cityroam', na=False, case=False)
}

# Add the "Other" category
all_matches = pd.Series(False, index=data_filtered.index)
for category, mask in categories.items():
    all_matches |= mask
categories["Other"] = ~all_matches

# Initialize the map centered around the US
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Initialize a MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

# List to store the marker objects for filtering
markers = []

# Initialize category counts
category_counts = {cat: 0 for cat in categories.keys()}

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
    
    marker_categories = {cat: bool(categories[cat].iloc[idx]) for cat in categories}
    markers.append({
        'latlng': [row['trilat'], row['trilong']],
        'popup': popup_text,
        'categories': marker_categories,
        'ssid': row['ssid'] if isinstance(row['ssid'], str) else '',
        'rcois': row['rcois']
    })
    
    # Increment counts for each category
    for cat, is_match in marker_categories.items():
        if is_match:
            category_counts[cat] += 1

# Calculate total count
total_count = len(markers)

# Add the total count display and category counts
category_counts_html = "".join([f"<br><span class='category-count' id='count-{cat}'>{cat}: {count}</span>" for cat, count in category_counts.items()])

total_count_html = f"""
<div class="count-container" style="position: fixed; top: 25px; left: 25px; width: 200px; z-index: 1000; background: white; padding: 25px; border: 1px solid black;">
    Total Nodes: <span id="total-count">{total_count}</span>
    {category_counts_html}
    <br><span class='category-count' id='visible-count'>Visible Nodes: {total_count}</span>
</div>
"""
m.get_root().html.add_child(folium.Element(total_count_html))

# Add the category checkboxes
checkbox_html = """
<div class="filter-container" style="position: fixed; top: 25px; right: 25px; width: 200px; z-index: 1000; background: white; padding: 25px; border: 1px solid black;">
    <h4>Categories</h4>
"""
for category in categories.keys():
    checkbox_html += f'<label><input type="checkbox" class="category-checkbox" value="{category}" checked> {category}</label><br>'
checkbox_html += '<button onclick="applyFilter()">Apply</button></div>'

# Add search by SSID and RCOI
search_html = """
<div class="search-container" style="position: fixed; top: 500px; right: 25px; width: 200px; z-index: 1000; background: white; padding: 25px; border: 1px solid black;">
    <h4>Search</h4>
    <label for="ssid-search">SSID:</label>
    <input type="text" id="ssid-search" class="search-input" style="padding-left: 10px; padding-right: 10px; max-width: 80%;"><br>
    <label for="rcoi-search">RCOI:</label>
    <input type="text" id="rcoi-search" class="search-input" style="padding-left: 10px; padding-right: 10px; max-width: 80%;"><br>
    <label for="use-regex">Use Regex:</label>
    <input type="checkbox" id="use-regex" class="search-input"><br>
    <button onclick="applySearch()">Search</button>
    <br>
    Matched Nodes: <span id="search-count">0</span>
</div>
"""
m.get_root().html.add_child(folium.Element(checkbox_html + search_html))

# Add custom CSS for responsive design
responsive_css = """
<style>
@media (max-width: 768px) {
    .filter-container, .search-container, .category-count {
        display: none;
    }
    .count-container {
        width: 150px;
    }
}
</style>
"""
m.get_root().html.add_child(folium.Element(responsive_css))

# Add custom JavaScript for dynamic filtering and count updating
custom_script = f"""
<script>
    var markers = {json.dumps(markers)};
    
    function getMapInstance() {{
        return Object.values(window).find(val => val instanceof L.Map);
    }}
    
    function updateCounts(filteredMarkers) {{
        var categoryCounts = {json.dumps(category_counts)};
        var counts = {{}};
        
        Object.keys(categoryCounts).forEach(cat => {{
            counts[cat] = 0;
        }});

        filteredMarkers.forEach(marker_obj => {{
            Object.keys(marker_obj.categories).forEach(cat => {{
                if (marker_obj.categories[cat]) {{
                    counts[cat]++;
                }}
            }});
        }});
        
        Object.keys(counts).forEach(cat => {{
            var countElem = document.getElementById('count-' + cat);
            if (countElem) {{
                if (counts[cat] > 0) {{
                    countElem.style.display = '';
                    countElem.innerText = cat + ': ' + counts[cat];
                }} else {{
                    countElem.style.display = 'none';
                }}
            }}
        }});
        
        document.getElementById('visible-count').innerText = 'Visible Nodes: ' + filteredMarkers.length;
    }}

    function updateVisibleCount() {{
        var map = getMapInstance();
        var bounds = map.getBounds();
        var visibleMarkers = markers.filter(function(marker_obj) {{
            return bounds.contains(marker_obj.latlng);
        }});
        document.getElementById('visible-count').innerText = 'Visible Nodes: ' + visibleMarkers.length;
    }}

    function applyFilter() {{
        var map = getMapInstance();
        var filteredMarkers = [];
        var selectedCategories = Array.from(document.querySelectorAll('.category-checkbox:checked')).map(cb => cb.value);

        {marker_cluster.get_name()}.clearLayers();
        
        markers.forEach(function(marker_obj) {{
            var match = selectedCategories.some(function(category) {{
                return marker_obj.categories[category];
            }});
            
            if (match) {{
                var marker = L.marker(marker_obj.latlng).bindPopup(marker_obj.popup);
                marker.addTo({marker_cluster.get_name()});
                filteredMarkers.push(marker_obj);
            }}
        }});

        updateCounts(filteredMarkers);
        updateVisibleCount();
    }}

    function applySearch() {{
        var map = getMapInstance();
        var ssidSearch = document.getElementById('ssid-search').value;
        var rcoiSearch = document.getElementById('rcoi-search').value;
        var useRegex = document.getElementById('use-regex').checked;

        var regexFlags = 'i';
        var ssidRegex = new RegExp(ssidSearch, regexFlags);
        var rcoiRegex = new RegExp(rcoiSearch, regexFlags);

        var matchedMarkers = [];
        {marker_cluster.get_name()}.clearLayers();

        markers.forEach(function(marker_obj) {{
            var ssidMatch = useRegex ? ssidRegex.test(marker_obj.ssid) : marker_obj.ssid.toLowerCase().includes(ssidSearch.toLowerCase());
            var rcoiMatch = useRegex ? rcoiRegex.test(marker_obj.rcois) : marker_obj.rcois.toLowerCase().includes(rcoiSearch.toLowerCase());

            if (ssidMatch && rcoiMatch) {{
                var marker = L.marker(marker_obj.latlng).bindPopup(marker_obj.popup);
                marker.addTo({marker_cluster.get_name()});
                matchedMarkers.push(marker_obj);
            }}
        }});

        document.getElementById('search-count').innerText = matchedMarkers.length;

        // Uncheck all category options
        document.querySelectorAll('.category-checkbox').forEach(cb => {{
            cb.checked = false;
        }});

        updateCounts(matchedMarkers);
        updateVisibleCount();
    }}

    document.addEventListener('DOMContentLoaded', function() {{
        var map = getMapInstance();
        map.on('moveend', updateVisibleCount);
    }});
</script>
"""
m.get_root().html.add_child(folium.Element(custom_script))

# Save the map to an HTML file in the Output folder
map_file_path = os.path.join(output_path, 'wigle_map.html')
docs_index_path = os.path.join(docs_path, 'index.html')
archive_file_path = os.path.join(archive_path, f'wigle_map_{current_year}.html')

m.save(map_file_path)
m.save(docs_index_path)
m.save(archive_file_path)

print(f"Map has been saved to {map_file_path} and archived to {archive_file_path}")
