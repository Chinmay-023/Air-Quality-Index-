# Data Dictionary

## Table: hourly_air_quality
- `id` (SERIAL): Primary Key.
- `timestamp` (TIMESTAMP WITH TIME ZONE): UTC time of the reading.
- `station` (VARCHAR): Station name.
- `city` (VARCHAR): City name.
- `pm25` (FLOAT): Average PM2.5 concentration (ug/m3).
- `pm10` (FLOAT): Average PM10 concentration (ug/m3).
- `aqi` (FLOAT): Calculated AQI value.
- `aqi_category` (VARCHAR): AQI Category (e.g., 'Good', 'Poor').

## Table: hourly_weather
- `timestamp` (TIMESTAMP WITH TIME ZONE): UTC time of reading.
- `temperature_2m` (FLOAT): Air temperature in °C.
- `relative_humidity_2m` (FLOAT): Humidity in %.
- `wind_speed_10m` (FLOAT): Wind speed in km/h.
- `precipitation` (FLOAT): Precipitation in mm.

## Table: model_predictions
- `prediction_timestamp` (TIMESTAMP): When prediction was made.
- `target_date` (DATE): Date the prediction applies to.
- `predicted_aqi` (FLOAT): Predicted AQI.
- `actual_aqi` (FLOAT): True AQI (updated later).
- `model_version` (VARCHAR): Model URI or version ID.
