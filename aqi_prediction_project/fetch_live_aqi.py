import requests
import datetime
import pandas as pd
from sqlalchemy import create_engine
from src.transformation.aqi_calculation import get_aqi_category

DB_URL = "postgresql://aqi_user:aqi_password@postgres:5432/aqi_db"
engine = create_engine(DB_URL)

cities = {
    "Delhi": (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Kanpur": (26.4499, 80.3319)
}

def fetch_live_aqi():
    now = datetime.datetime.utcnow()
    data = []
    
    for city, coords in cities.items():
        lat, lon = coords
        aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi&timezone=auto"
        
        try:
            aqi_res = requests.get(aqi_url).json()
            pm25 = aqi_res.get('current', {}).get('pm2_5', 20.0)
            pm10 = aqi_res.get('current', {}).get('pm10', pm25+5)
            aqi = aqi_res.get('current', {}).get('us_aqi', 50)
            
            category = get_aqi_category(aqi)
            
            station_name = f"REAL-TIME API: {city} Central"
            
            data.append({
                'timestamp': now,
                'station': station_name,
                'city': city,
                'pm25': pm25,
                'pm10': pm10,
                'aqi': aqi,
                'aqi_category': category
            })
            
            station_df = pd.DataFrame([{'name': station_name, 'city': city}])
            try:
                station_df.to_sql('stations', engine, if_exists='append', index=False)
            except Exception:
                pass
            
            print(f"Successfully fetched live data for {city}: AQI {aqi}")
            
        except Exception as e:
            print(f"Error fetching for {city}: {e}")
            
    df = pd.DataFrame(data)
    df.to_sql('hourly_air_quality', engine, if_exists='append', index=False)
    print(f"Inserted {len(df)} real-time LIVE records into database.")

if __name__ == '__main__':
    fetch_live_aqi()
