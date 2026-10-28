import pandas as pd
from src.utils.logger import get_logger

logger = get_logger("aggregation")

def aggregate_openaq_to_hourly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates long-format OpenAQ data to wide-format hourly data."""
    if df.empty:
        return pd.DataFrame()
        
    df['timestamp'] = df['timestamp'].dt.floor('H')
    
    pivoted = df.pivot_table(
        index=['timestamp', 'station', 'city'],
        columns='pollutant',
        values='value',
        aggfunc='mean'
    ).reset_index()
    
    pivoted.columns.name = None
    pivoted.rename(columns=lambda x: x.lower(), inplace=True)
    
    logger.info(f"Aggregated OpenAQ to {len(pivoted)} hourly records.")
    return pivoted
