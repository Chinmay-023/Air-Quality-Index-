import pandas as pd
import numpy as np

def calculate_sub_index_pm25(pm25):
    if pd.isna(pm25) or pm25 < 0: return 0
    if pm25 <= 30: return pm25 * 50 / 30
    elif pm25 <= 60: return 50 + (pm25 - 30) * 50 / 30
    elif pm25 <= 90: return 100 + (pm25 - 60) * 100 / 30
    elif pm25 <= 120: return 200 + (pm25 - 90) * 100 / 30
    elif pm25 <= 250: return 300 + (pm25 - 120) * 100 / 130
    else: return 400 + (pm25 - 250) * 100 / 130

def calculate_sub_index_pm10(pm10):
    if pd.isna(pm10) or pm10 < 0: return 0
    if pm10 <= 50: return pm10
    elif pm10 <= 100: return pm10
    elif pm10 <= 250: return 100 + (pm10 - 100) * 100 / 150
    elif pm10 <= 350: return 200 + (pm10 - 250) * 100 / 100
    elif pm10 <= 430: return 300 + (pm10 - 350) * 100 / 80
    else: return 400 + (pm10 - 430) * 100 / 80

def get_aqi_category(aqi):
    if pd.isna(aqi): return 'Unknown'
    if aqi <= 50: return 'Good'
    elif aqi <= 100: return 'Moderate'
    elif aqi <= 150: return 'Poor'
    elif aqi <= 200: return 'Unhealthy'
    elif aqi <= 300: return 'Severe'
    else: return 'Hazardous'

def calculate_aqi(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    if 'pm25' in df.columns:
        df['sub_index_pm25'] = df['pm25'].apply(calculate_sub_index_pm25)
    else:
        df['sub_index_pm25'] = 0
        
    if 'pm10' in df.columns:
        df['sub_index_pm10'] = df['pm10'].apply(calculate_sub_index_pm10)
    else:
        df['sub_index_pm10'] = 0
        
    df['aqi'] = df[['sub_index_pm25', 'sub_index_pm10']].max(axis=1)
    df.loc[(df['sub_index_pm25'] == 0) & (df['sub_index_pm10'] == 0), 'aqi'] = np.nan
    df['aqi_category'] = df['aqi'].apply(get_aqi_category)
    return df
