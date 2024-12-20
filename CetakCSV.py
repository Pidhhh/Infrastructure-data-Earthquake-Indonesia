import requests
import pandas as pd
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# Base URL for USGS Earthquake API
USGS_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Define the bounds for Indonesia (approximate)
MIN_LAT, MAX_LAT = -11.0, 6.0  # Latitude range for Indonesia
MIN_LON, MAX_LON = 95.0, 141.0  # Longitude range for Indonesia

def fetch_earthquake_data(starttime, endtime, min_magnitude=0, max_magnitude=None, format="geojson", limit=20000):
    """
    Fetch earthquake data from the USGS API.
    Args:
        starttime (str): Start time in ISO8601 format (e.g., "2020-01-01").
        endtime (str): End time in ISO8601 format (e.g., "2024-12-01").
        min_magnitude (float): Minimum magnitude of earthquakes to fetch.
        max_magnitude (float): Maximum magnitude of earthquakes to fetch.
        format (str): Response format (e.g., 'geojson', 'csv').
        limit (int): Maximum number of events to retrieve.
    Returns:
        dict or None: Parsed JSON response if format is "geojson"; None otherwise.
    """
    params = {
        "format": format,
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": min_magnitude,
        "limit": limit,
    }
    if max_magnitude:
        params["maxmagnitude"] = max_magnitude
    
    try:
        response = requests.get(USGS_BASE_URL, params=params)
        response.raise_for_status()
        if format == "geojson":
            return response.json()
        else:
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from USGS API: {e}")
        return None

def parse_earthquake_data(data):
    """
    Parse earthquake data from GeoJSON format and filter for Indonesia.
    Args:
        data (dict): GeoJSON data from the USGS API.
    Returns:
        list[dict]: Parsed list of earthquake events.
    """
    if not data or "features" not in data:
        print("No data available.")
        return []
    
    earthquakes = []
    for feature in data["features"]:
        properties = feature["properties"]
        geometry = feature["geometry"]
        
        # Check if the earthquake is within Indonesia's geographic bounds
        if (geometry and geometry["coordinates"] and
                MIN_LAT <= geometry["coordinates"][1] <= MAX_LAT and
                MIN_LON <= geometry["coordinates"][0] <= MAX_LON):
            # Convert timestamp to a readable format
            timestamp_ms = properties.get("time")
            readable_time = None
            if timestamp_ms:
                unix_timestamp_s = timestamp_ms / 1000
                readable_time = datetime.utcfromtimestamp(unix_timestamp_s).strftime("%Y-%m-%d %H:%M:%S")
            
            earthquakes.append({
                "Time": readable_time,
                "Place": properties.get("place"),
                "Magnitude": properties.get("mag"),
                "Depth (km)": geometry["coordinates"][2] if geometry and geometry["coordinates"] else None,
                "Longitude": geometry["coordinates"][0] if geometry and geometry["coordinates"] else None,
                "Latitude": geometry["coordinates"][1] if geometry and geometry["coordinates"] else None,
            })
    return earthquakes

def save_to_csv(data, filename):
    """
    Save earthquake data to a CSV file.
    Args:
        data (list[dict]): Parsed earthquake data.
        filename (str): Output CSV file name.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def fetch_and_save_earthquake_data():
    """Fetch data and save it to CSV every time the scheduler triggers"""
    # Define the date range and magnitude filters
    start_date = "2020-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")  # Up to the current date
    min_magnitude = 5.0  # Example filter for significant earthquakes
    
    print(f"Fetching earthquake data from {start_date} to {end_date}...")
    data = fetch_earthquake_data(
        starttime=start_date, 
        endtime=end_date, 
        min_magnitude=min_magnitude
    )
    
    if data:
        parsed_data = parse_earthquake_data(data)
        filename = f"indonesia_earthquake_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        save_to_csv(parsed_data, filename)

def main():
    # Create an APScheduler instance
    scheduler = BlockingScheduler()

    # Add a job to fetch and save earthquake data every 30 
    scheduler.add_job(fetch_and_save_earthquake_data, 'interval', seconds=30)

    # Start the scheduler
    print("Scheduler started. Fetching earthquake data every 30 second.")
    scheduler.start()

if __name__ == "__main__":
    main()