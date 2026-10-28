import os
import json
import requests
import datetime
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.config import CONFIG, get_project_root, OPENAQ_API_KEY

logger = get_logger("openaq_client")

class OpenAQClient:
    def __init__(self):
        self.base_url = CONFIG["data_collection"]["openaq"]["base_url"]
        self.city = CONFIG["location"]["city"]
        self.parameters = CONFIG["pollutants"]
        self.headers = {"X-API-Key": OPENAQ_API_KEY} if OPENAQ_API_KEY else {}

    def fetch_data(self, date_from: str, date_to: str) -> dict:
        """
        Fetch air quality data from OpenAQ API.
        Dates should be in ISO format (YYYY-MM-DDTHH:MM:SSZ)
        """
        logger.info(f"Fetching OpenAQ data for {self.city} from {date_from} to {date_to}")
        
        endpoint = f"{self.base_url}/measurements"
        
        params = {
            "city": self.city,
            "date_from": date_from,
            "date_to": date_to,
            "limit": 10000,
            "page": 1,
            "order_by": "datetime"
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            logger.info(f"Successfully fetched {len(results)} records from OpenAQ API. Status: {response.status_code}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from OpenAQ: {e}")
            return {"meta": {"name": "openaq-api", "found": 0}, "results": [], "error": str(e)}

    def save_raw_data(self, data: dict, extraction_timestamp: str) -> str:
        """Save raw API response to data/raw directory"""
        raw_dir = get_project_root() / "data" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"openaq_raw_{extraction_timestamp}.json"
        filepath = raw_dir / filename
        
        metadata = {
            "extraction_timestamp": extraction_timestamp,
            "source": "OpenAQ API v2",
            "row_count": len(data.get("results", [])),
            "status": "success" if "error" not in data else "error",
            "error_message": data.get("error", None)
        }
        data["_metadata"] = metadata
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Saved raw OpenAQ data to {filepath}")
        return str(filepath)

if __name__ == "__main__":
    client = OpenAQClient()
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=1)
    
    data = client.fetch_data(
        date_from=start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        date_to=end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    client.save_raw_data(data, timestamp)
