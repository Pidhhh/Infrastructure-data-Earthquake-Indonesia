import requests
import pandas as pd
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from tkinter import Tk, Label, Button, StringVar, ttk, messagebox

# Base URL for USGS Earthquake API
USGS_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Define the bounds for Indonesia (approximate)
MIN_LAT, MAX_LAT = -11.0, 6.0  # Latitude range for Indonesia
MIN_LON, MAX_LON = 95.0, 141.0  # Longitude range for Indonesia

class EarthquakeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Indonesia Earthquake Tracker")
        self.status_var = StringVar(value="Press 'Start' to begin fetching earthquake data.")
        self.data = []
        
        # UI Elements
        self.create_widgets()
        
        # Background Scheduler
        self.scheduler = BackgroundScheduler()

    def create_widgets(self):
        # Status label
        Label(self.root, textvariable=self.status_var, wraplength=400, justify="center").pack(pady=10)
        
        # Start/Stop buttons
        Button(self.root, text="Start", command=self.start_fetching).pack(side="left", padx=10)
        Button(self.root, text="Stop", command=self.stop_fetching).pack(side="left", padx=10)
        
        # Table
        self.tree = ttk.Treeview(self.root, columns=("Time", "Place", "Magnitude", "Depth", "Longitude", "Latitude"), show="headings")
        for col in ("Time", "Place", "Magnitude", "Depth", "Longitude", "Latitude"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10, fill="both", expand=True)
        
    def fetch_and_update_data(self):
        self.status_var.set("Fetching earthquake data...")
        start_date = "2020-01-01"
        end_date = datetime.now().strftime("%Y-%m-%d")
        min_magnitude = 5.0

        data = self.fetch_earthquake_data(
            starttime=start_date, 
            endtime=end_date, 
            min_magnitude=min_magnitude
        )
        if data:
            self.data = self.parse_earthquake_data(data)
            self.update_table(self.data)
            self.status_var.set(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def fetch_earthquake_data(self, starttime, endtime, min_magnitude=0, max_magnitude=None, format="geojson", limit=20000):
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
            return response.json() if format == "geojson" else response.text
        except requests.exceptions.RequestException as e:
            self.status_var.set(f"Error fetching data: {e}")
            return None

    def parse_earthquake_data(self, data):
        if not data or "features" not in data:
            return []

        earthquakes = []
        for feature in data["features"]:
            properties = feature["properties"]
            geometry = feature["geometry"]

            if (geometry and geometry["coordinates"] and
                    MIN_LAT <= geometry["coordinates"][1] <= MAX_LAT and
                    MIN_LON <= geometry["coordinates"][0] <= MAX_LON):
                timestamp_ms = properties.get("time")
                readable_time = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S") if timestamp_ms else None
                
                earthquakes.append({
                    "Time": readable_time,
                    "Place": properties.get("place"),
                    "Magnitude": properties.get("mag"),
                    "Depth (km)": geometry["coordinates"][2],
                    "Longitude": geometry["coordinates"][0],
                    "Latitude": geometry["coordinates"][1],
                })
        return earthquakes

    def update_table(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for entry in data:
            self.tree.insert("", "end", values=(entry["Time"], entry["Place"], entry["Magnitude"],
                                                entry["Depth (km)"], entry["Longitude"], entry["Latitude"]))

    def start_fetching(self):
        if not self.scheduler.running:
            self.scheduler.add_job(self.fetch_and_update_data, 'interval', seconds=5)
            self.scheduler.start()
        self.status_var.set("Fetching started. Updates every 30 seconds.")

    def stop_fetching(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
        self.status_var.set("Fetching stopped.")

def main():
    root = Tk()
    app = EarthquakeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
