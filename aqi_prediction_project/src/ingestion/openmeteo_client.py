import os
import json
import requests
import datetime
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.config import CONFIG, get_project_root

logger = get_logger("openmeteo_client")

class OpenMeteoClient:
    def __init__(self):
        self.base_url = "https://archive-api.open-meteo.com/v1/archive"
        self.latitude = CONFIG["location"]["latitude"]
        self.longitude = CONFIG["location"]["longitude"]
        self.hourly_vars = CONFIG["weather_variables"]

    def fetch_data(self, start_date: str, end_date: str) -> dict:
        """
        Fetch historical weather data from Open-Meteo.
        Dates should be in YYYY-MM-DD format.
        """
        logger.info(f"Fetching Open-Meteo data for coords ({self.latitude}, {self.longitude}) from {start_date} to {end_date}")
        
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ",".join(self.hourly_vars),
            "timezone": "auto"
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            hours_count = len(data.get("hourly", {}).get("time", []))
            logger.info(f"Successfully fetched weather data for {hours_count} hours. Status: {response.status_code}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from Open-Meteo: {e}")
            return {"error": str(e), "hourly": {}}

    def save_raw_data(self, data: dict, extraction_timestamp: str) -> str:
        """Save raw API response to data/raw directory"""
        raw_dir = get_project_root() / "data" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"openmeteo_raw_{extraction_timestamp}.json"
        filepath = raw_dir / filename
        
        metadata = {
            "extraction_timestamp": extraction_timestamp,
            "source": "Open-Meteo Archive API",
            "row_count": len(data.get("hourly", {}).get("time", [])),
            "status": "success" if "error" not in data else "error",
            "error_message": data.get("error", None)
        }
        data["_metadata"] = metadata
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Saved raw Open-Meteo data to {filepath}")
        return str(filepath)

if __name__ == "__main__":
    client = OpenMeteoClient()
    end = datetime.datetime.now() - datetime.timedelta(days=2) 
    start = end - datetime.timedelta(days=7)
    
    data = client.fetch_data(
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d")
    )
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    client.save_raw_data(data, timestamp)
