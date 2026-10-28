import os
import sys
from datetime import datetime, timedelta

from src.ingestion.openaq_client import OpenAQClient
from src.ingestion.openmeteo_client import OpenMeteoClient
from src.transformation.cleaning import process_openaq_raw, process_openmeteo_raw
from src.transformation.validation import validate_openaq_data, save_rejected
from src.transformation.aggregation import aggregate_openaq_to_hourly
from src.transformation.aqi_calculation import calculate_aqi
from src.database.connection import init_db
from src.database.loader import load_dataframe_to_postgres
from src.utils.logger import get_logger

logger = get_logger("run_etl")

def run():
    init_db()
    
    # Extract
    client_aq = OpenAQClient()
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=1)
    
    data_aq = client_aq.fetch_data(
        date_from=start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        date_to=end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    openaq_file = client_aq.save_raw_data(data_aq, timestamp)
    
    client_w = OpenMeteoClient()
    end_date_w = datetime.now()
    start_date_w = end_date_w - timedelta(days=7)
    
    data_w = client_w.fetch_data(
        start_date=start_date_w.strftime("%Y-%m-%d"),
        end_date=end_date_w.strftime("%Y-%m-%d")
    )
    openmeteo_file = client_w.save_raw_data(data_w, timestamp)
    
    # Transform and Load
    if openaq_file:
        raw_df = process_openaq_raw(openaq_file)
        valid_df, rejected_df = validate_openaq_data(raw_df)
        save_rejected(rejected_df, "openaq")
        
        hourly_df = aggregate_openaq_to_hourly(valid_df)
        aqi_df = calculate_aqi(hourly_df)
        
        aqi_df.drop_duplicates(subset=['timestamp', 'station'], inplace=True)
        load_dataframe_to_postgres(aqi_df, 'hourly_air_quality', if_exists='append')
        
        if not valid_df.empty:
            stations_df = valid_df[['station', 'city']].drop_duplicates()
            stations_df.rename(columns={'station': 'name'}, inplace=True)
            load_dataframe_to_postgres(stations_df, 'stations', if_exists='append')
            
    if openmeteo_file:
        weather_df = process_openmeteo_raw(openmeteo_file)
        if not weather_df.empty:
            weather_df.drop_duplicates(subset=['timestamp'], inplace=True)
            load_dataframe_to_postgres(weather_df, 'hourly_weather', if_exists='append')
            
    logger.info("ETL completed.")

if __name__ == "__main__":
    run()
