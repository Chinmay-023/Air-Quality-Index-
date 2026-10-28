import pandas as pd
import json
from src.utils.logger import get_logger

logger = get_logger("cleaning")

def process_openaq_raw(filepath: str) -> pd.DataFrame:
    """Process raw OpenAQ JSON into a normalized DataFrame."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if "results" not in data or not data["results"]:
            logger.warning(f"No results found in {filepath}")
            return pd.DataFrame()
            
        df = pd.json_normalize(data["results"])
        
        rename_map = {
            'location': 'station',
            'parameter': 'pollutant',
            'value': 'value',
            'unit': 'unit',
            'date.utc': 'timestamp',
            'city': 'city'
        }
        
        cols_to_keep = [c for c in rename_map.keys() if c in df.columns]
        df = df[cols_to_keep].rename(columns=rename_map)
        
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
            
        return df
    except Exception as e:
        logger.error(f"Error processing OpenAQ raw file {filepath}: {e}")
        return pd.DataFrame()

def process_openmeteo_raw(filepath: str) -> pd.DataFrame:
    """Process raw Open-Meteo JSON into a normalized DataFrame."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        if "hourly" not in data or not data["hourly"]:
            logger.warning(f"No hourly data found in {filepath}")
            return pd.DataFrame()
            
        df = pd.DataFrame(data["hourly"])
        
        if 'time' in df.columns:
            df['timestamp'] = pd.to_datetime(df['time'], errors='coerce', utc=True)
            df.drop('time', axis=1, inplace=True)
            
        return df
    except Exception as e:
        logger.error(f"Error processing Open-Meteo raw file {filepath}: {e}")
        return pd.DataFrame()
