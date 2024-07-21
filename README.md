# Track OpenRoaming Passpoint

A collection of scripts and tools that tracks the availability of Hotspot 2.0, Passpoint, and OpenRoaming networks in the wild.

### OpenRoaming and Hotspot 2.0 Stats Table

<!-- STATS START -->

| Statistic | Count | Description |
|-----------|-------|-------------|
| Total Hotspot 2.0 APs | 14153 | Total count of all Hotspot 2.0 access points |
| OpenRoaming Unsettled | 3064 | Count of devices with RCOI containing '5a03ba' |
| OpenRoaming Settled | 42 | Count of devices with RCOI containing 'baa2d' but not '5a03ba' |
| Google Orion Devices | 7694 | Count of devices with RCOI containing 'f4f5e8f5f4' |
| XNET Devices | 137 | Count of devices with SSID containing 'XNET' |
| Helium Devices | 5 | Count of devices with SSID containing 'HELIUM' |
| Other Devices | 3211 | Count of devices that do not match any of the above categories |

<!-- STATS END -->

## Table of Contents

- [Track OpenRoaming Passpoint](#track-openroaming-passpoint)
    - [OpenRoaming and Hotspot 2.0 Stats Table](#openroaming-and-hotspot-20-stats-table)
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
