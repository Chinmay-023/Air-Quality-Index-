CREATE TABLE IF NOT EXISTS stations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    city VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS hourly_air_quality (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    station VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    pm25 FLOAT,
    pm10 FLOAT,
    no2 FLOAT,
    so2 FLOAT,
    co FLOAT,
    o3 FLOAT,
    sub_index_pm25 FLOAT,
    sub_index_pm10 FLOAT,
    aqi FLOAT,
    aqi_category VARCHAR(50),
    UNIQUE(timestamp, station)
);

CREATE TABLE IF NOT EXISTS hourly_weather (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    temperature_2m FLOAT,
    relative_humidity_2m FLOAT,
    precipitation FLOAT,
    wind_speed_10m FLOAT,
    wind_direction_10m FLOAT,
    surface_pressure FLOAT,
    UNIQUE(timestamp)
);

CREATE TABLE IF NOT EXISTS model_predictions (
    id SERIAL PRIMARY KEY,
    prediction_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    target_date DATE NOT NULL,
    predicted_aqi FLOAT,
    predicted_category VARCHAR(50),
    actual_aqi FLOAT,
    model_version VARCHAR(100)
);

CREATE OR REPLACE VIEW daily_air_quality AS
SELECT 
    DATE(timestamp) as date,
    station,
    city,
    AVG(pm25) as avg_pm25,
    AVG(pm10) as avg_pm10,
    MAX(aqi) as max_aqi,
    AVG(aqi) as avg_aqi
FROM hourly_air_quality
GROUP BY DATE(timestamp), station, city;
