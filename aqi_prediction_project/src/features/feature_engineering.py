import pandas as pd
from sqlalchemy import create_engine
from src.database.connection import get_engine
from src.utils.logger import get_logger

logger = get_logger("feature_engineering")

def fetch_data_for_features() -> pd.DataFrame:
    query = """
    SELECT 
        a.timestamp,
        DATE(a.timestamp) as date,
        a.station,
        a.aqi,
        a.pm25,
        a.pm10,
        a.no2,
        a.so2,
        a.co,
        a.o3,
        a.aqi_category,
        w.temperature_2m as temperature,
        w.relative_humidity_2m as humidity,
        w.wind_speed_10m as wind_speed,
        w.precipitation
    FROM hourly_air_quality a
    LEFT JOIN hourly_weather w ON a.timestamp = w.timestamp
    ORDER BY a.station, a.timestamp
    """
    engine = get_engine()
    df = pd.read_sql(query, engine)
    logger.info(f"Fetched {len(df)} rows for feature engineering.")
    return df

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
        
    df = df.copy()
    df = df.sort_values(by=['station', 'timestamp']).reset_index(drop=True)
    
    daily_df = df.groupby(['station', 'date']).agg({
        'aqi': 'mean',
        'pm25': 'mean',
        'pm10': 'mean',
        'no2': 'mean',
        'so2': 'mean',
        'co': 'mean',
        'o3': 'mean',
        'temperature': 'mean',
        'humidity': 'mean',
        'wind_speed': 'mean',
        'precipitation': 'sum'
    }).reset_index()
    
    daily_df = daily_df.sort_values(by=['station', 'date'])
    
    for col in ['aqi', 'pm25', 'pm10', 'no2', 'so2', 'co', 'o3']:
        daily_df[f'{col}_lag_1'] = daily_df.groupby('station')[col].shift(1)
        if col == 'aqi':
            daily_df[f'{col}_lag_2'] = daily_df.groupby('station')[col].shift(2)
            daily_df[f'{col}_lag_3'] = daily_df.groupby('station')[col].shift(3)
            daily_df[f'{col}_lag_7'] = daily_df.groupby('station')[col].shift(7)
            
            daily_df['aqi_rolling_mean_3'] = daily_df.groupby('station')[col].rolling(window=3, min_periods=1).mean().reset_index(0, drop=True)
            daily_df['aqi_rolling_mean_7'] = daily_df.groupby('station')[col].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
            daily_df['aqi_rolling_std_7'] = daily_df.groupby('station')[col].rolling(window=7, min_periods=1).std().reset_index(0, drop=True)
            
    daily_df['target_next_day_aqi'] = daily_df.groupby('station')['aqi'].shift(-1)
    
    from src.transformation.aqi_calculation import get_aqi_category
    daily_df['target_category'] = daily_df['target_next_day_aqi'].apply(get_aqi_category)
    
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    daily_df['day'] = daily_df['date'].dt.day
    daily_df['month'] = daily_df['date'].dt.month
    daily_df['day_of_week'] = daily_df['date'].dt.dayofweek
    daily_df['is_weekend'] = daily_df['day_of_week'].isin([5, 6]).astype(int)
    
    daily_df = daily_df.dropna(subset=['target_next_day_aqi', 'aqi_lag_1'])
    
    logger.info(f"Generated features for {len(daily_df)} daily records.")
    return daily_df
