# Infrastructure-data-Earthquake-Indonesia

## Group Members
- Cesario Hafidh Arifa Noorcholish (L200224217)
- Muhammad Yusi Raykhan Nur (L200224266)

Infrastructure Sains Group Assignment. This group focuses on streaming earthquake data using the USGS API and creating a GUI to show the map.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/Infrastructure-data-Earthquake-Indonesia.git
    cd Infrastructure-data-Earthquake-Indonesia
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application:**
    ```sh
    python Main.py
    ```

2. **Using the GUI:**
    - Press the "Start" button to begin fetching earthquake data.
    - The data will be updated every 30 seconds.
    - Press the "Stop" button to stop fetching data.
    - The table will display the latest earthquake data.
    - The map will show the locations of the earthquakes.

## Requirements

- Python 3.6 or higher
- Required Python packages (listed in `requirements.txt`):
    - requests
    - pandas
    - apscheduler
    - tkinter
    - matplotlib
    - cartopy

## License

This project is licensed under the MIT License.
