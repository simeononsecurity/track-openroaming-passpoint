# Track OpenRoaming Passpoint

[![Sponsor](https://img.shields.io/badge/Sponsor-Click%20Here-ff69b4)](https://github.com/sponsors/simeononsecurity) [![Interactive Map](https://img.shields.io/badge/Interactive%20Map-View%20Here-blue)](https://openroamingmap.simeononsecurity.com)

A collection of scripts and tools that tracks the availability of Hotspot 2.0, Passpoint, and OpenRoaming networks in the wild.

Pulls from the Wigle.net dataset. 

> **Note**: Information here may not be entirely accurate or complete, but it's the best semi-public dataset available for tracking this kind of information. 
The stats are dynamic, we only pull year to date stats. But ultimately we'll update it to do devices mapped in the last 365 days.

> **Note:**: All of the categorizations and identifiers were discovered from public documentation and research that is repeatable with google searches. 

<!-- STATS START -->

### OpenRoaming and Hotspot 2.0 Stats Table
| Statistic | Count | Description |
|-----------|-------|-------------|
| Total Hotspot 2.0 APs | 23457 | Total count of all Hotspot 2.0 access points |
| OpenRoaming Unsettled | 6826 | Count of devices with RCOI matching any OpenRoaming unsettled RCOI |
| OpenRoaming Settled | 292 | Count of devices with RCOI matching any OpenRoaming settled RCOI |
| EDUROAM Devices | 628 | Count of devices with RCOI containing either '5A03BA0800' or '1BC50460' or with an SSID matching "eduroam" |
| Google Orion Devices | 10405 | Count of devices with RCOI containing 'f4f5e8f5f4' |
| IronWiFi Devices | 161 | Count of devices with RCOI containing 'aa146b0000' |
| XNET Devices | 231 | Count of devices with SSID containing 'XNET' |
| Helium Devices | 15 | Count of devices with SSID containing 'Helium Mobile' |
| Wayru Devices | 0 | Count of devices with SSID containing 'Wayru' |
| MetaBlox Devices | 7 | Count of devices with SSID containing 'MetaBlox' |
| CityRoam Devices | 904 | Count of devices with SSID containing 'cityroam' |
| Other Devices | 11005 | Count of devices that do not match any of the above categories |


### Most Common RCOI Enabled SSIDs
| SSID | Count |
|------|-------|
| BoldynPasspoint | 3517 |
| Cellular Wi-Fi Passthrough | 2098 |
| LiveBetter | 1936 |
| .p | 1683 |
| adco | 1067 |
| Xfinity Mobile | 1063 |
| GPGMS_CarrierOffloading | 954 |
| Passpoint WiFi | 945 |
| cityroam | 902 |
| Orion | 891 |

### Unique RCOIs
| RCOI | Definition | Count |
|------|------------|-------|
| 112233 | Unknown | 1 |
| 1122330000 | Unknown | 16 |
| 1834af | Unknown | 241 |
| 1bc50460 | Unknown | 614 |
| 1bc5046f | Unknown | 28 |
| 1bc504bd | Unknown | 48 |
| 21122 | Unknown | 1153 |
| 2233445566 | Unknown | 1294 |
| 24e4ce | Unknown | 7 |
| 310280 | ATT Offload ? | 3817 |
| 310410 | ATT Offload ? | 3839 |
| 313100 | ATT Offload ? | 3839 |
| 3213445172 | Unknown | 44 |
| 3af050201 | Unknown | 11 |
| 3af521 | SingleDigits Testing RCOI | 962 |
| 40202 | Unknown | 2 |
| 4096 | OpenRoaming Unsettled | 6632 |
| 445566 | Unknown | 1 |
| 500b | OpenRoaming Unsettled | 13 |
| 500f | OpenRoaming Settled | 97 |
| 506f9a | Unknown | 48 |
| 5a03ba | OpenRoaming Unsettled | 451 |
| 5a03ba0000 | OpenRoaming Unsettled | 6688 |
| 5a03ba0100 | OpenRoaming Unsettled | 4 |
| 5a03ba0600 | OpenRoaming Unsettled | 2 |
| 5a03ba0800 | OpenRoaming Unsettled | 6 |
| 5a03ba1000 | OpenRoaming Unsettled | 28 |
| 6a1f6c | Unknown | 520 |
| 840112 | Unknown | 1 |
| a43 | Unknown | 1 |
| aa146b | Unknown | 27 |
| aa146b0000 | IronWiFi Devices | 161 |
| baa2d0 | OpenRoaming Settled | 97 |
| baa2d00000 | OpenRoaming Settled | 277 |
| baa2d00100 | OpenRoaming Settled | 37 |
| baa2d06000 | OpenRoaming Settled | 2 |
| c | Unknown | 25 |
| cae505 | Unknown | 3944 |
| da9d490000 | Unknown | 1 |
| da9d490005 | Unknown | 1 |
| f4f5e8f5d4 | Unknown | 1 |
| f4f5e8f5e4 | Unknown | 1 |
| f4f5e8f5f4 | Google Orion Devices | 10405 |

<!-- STATS END -->

### OpenRoaming and Hotspot 2.0 Table Mapped

![OpenRoaming and Hotspot 2.0 Table Map](https://github.com/simeononsecurity/track-openroaming-passpoint/blob/main/output/global_wifi_map.png)

## Table of Contents

- [Track OpenRoaming Passpoint](#track-openroaming-passpoint)
    - [OpenRoaming and Hotspot 2.0 Stats Table](#openroaming-and-hotspot-20-stats-table)
    - [Most Common RCOI Enabled SSIDs](#most-common-rcoi-enabled-ssids)
    - [Unique RCOIs](#unique-rcois)
    - [OpenRoaming and Hotspot 2.0 Table Mapped](#openroaming-and-hotspot-20-table-mapped)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Scripts](#scripts)
      - [map\_wigle\_devices.py](#map_wigle_devicespy)
      - [filter\_sort\_wigle\_results.py](#filter_sort_wigle_resultspy)
      - [generate\_map\_html.py](#generate_map_htmlpy)
      - [generate\_map\_png.py](#generate_map_pngpy)
      - [update\_readme\_stats.py](#update_readme_statspy)
      - [classify\_locations.py](#classify_locationspy)
    - [Running the Scripts](#running-the-scripts)
  - [Automated Workflow](#automated-workflow)
    - [Workflow: `.github/workflows/update_statistics.yml`](#workflow-githubworkflowsupdate_statisticsyml)
  - [GitHub Pages](#github-pages)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

This project aims to track the availability of Hotspot 2.0, Passpoint, and OpenRoaming networks using data collected from WiGLE and other sources. The collected data is processed and visualized using various scripts.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/track-openroaming-passpoint.git
   cd track-openroaming-passpoint
   ```

2. Set up a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API credentials:
   ```env
   API_NAME=your_api_name
   API_TOKEN=your_api_token
   AUTH_HEADER=your_auth_header
   ```

## Usage

### Scripts

#### map_wigle_devices.py

Fetches data from the WiGLE API and saves it to a CSV file.

#### filter_sort_wigle_results.py

Filters and sorts the fetched WiGLE results and processes them for further analysis.

#### generate_map_html.py

Generates an interactive HTML map using Folium, displaying WiGLE data points. The HTML map files are saved to the `Output` directory and an `archive` subdirectory with the current year appended.

#### generate_map_png.py

Generates a static PNG map using Matplotlib and Basemap, displaying WiGLE data points. The PNG map files are saved to the `Output` directory and an `archive` subdirectory with the current year appended.

#### update_readme_stats.py

Updates the `README.md` file with statistics about the WiGLE data.

#### classify_locations.py

Classifies SSIDs from the WiGLE data as Residential, Business, or Public based on heuristics and performs reverse geocoding to add location information. The results are saved to a new CSV file.

### Running the Scripts

1. **Fetch data from WiGLE**:
   ```sh
   python scripts/map_wigle_devices.py
   ```

2. **Filter and sort the results**:
   ```sh
   python scripts/filter_sort_wigle_results.py
   ```

3. **Generate the HTML map**:
   ```sh
   python scripts/generate_map_html.py
   ```

4. **Generate the PNG map**:
   ```sh
   python scripts/generate_map_png.py
   ```

5. **Update the README with statistics**:
   ```sh
   python scripts/update_readme_stats.py
   ```

6. **Classify SSIDs and perform reverse geocoding**:
   ```sh
   python scripts/classify_locations.py
   ```

## Automated Workflow

The project includes a GitHub Actions workflow that runs the scripts automatically every 24 hours and updates the repository.

### Workflow: `.github/workflows/update_statistics.yml`

- Installs the pip requirements.
- Runs the scripts in order:
  - `map_wigle_devices.py`
  - `generate_map_html.py`
  - `generate_map_png.py`
  - `update_readme_stats.py`
- Commits the changes back to the repository.

## GitHub Pages

The HTML maps are made available through GitHub Pages. The workflow ensures the HTML files are copied to the `docs` folder, which is configured for GitHub Pages.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
