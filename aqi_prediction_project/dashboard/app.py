import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os
import requests

st.set_page_config(page_title="AQI Analysis & Prediction", layout="wide", page_icon="🌍")

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "aqi_db")
DB_USER = os.getenv("POSTGRES_USER", "aqi_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "aqi_password")
API_URL = os.getenv("API_URL", "http://localhost:8000")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

@st.cache_resource
def get_engine():
    return create_engine(DB_URL)

@st.cache_data(ttl=600)
def load_data(query):
    try:
        engine = get_engine()
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

st.title("🌍 Air Quality Index Analysis and Prediction")

st.sidebar.header("Filters")
cities_df = load_data("SELECT DISTINCT city FROM stations ORDER BY city")
city_list = cities_df['city'].tolist() if not cities_df.empty else ["Bengaluru"]
if "Bengaluru" in city_list:
    city_list.remove("Bengaluru")
    city_list.insert(0, "Bengaluru")
city = st.sidebar.selectbox("City", city_list, index=0, key="city_selector")

stations_df = load_data(f"SELECT name FROM stations WHERE city = '{city}' ORDER BY name")
station_list = stations_df['name'].tolist() if not stations_df.empty else []
if "AECS Layout" in station_list:
    station_list.remove("AECS Layout")
    station_list.insert(0, "AECS Layout")
station_list = ["All"] + station_list
station = st.sidebar.selectbox("Station", station_list, index=1 if "AECS Layout" in station_list else 0, key="station_selector")

tab1, tab2, tab3 = st.tabs(["📊 Current Analytics", "📈 Trends", "🔮 Predictions"])

with tab1:
    st.subheader("Current AQI Metrics")
    
    where_clause = f"WHERE city = '{city}'"
    if station != "All":
        where_clause = f"WHERE station = '{station}' AND city = '{city}'"
        
    query_latest = f"SELECT * FROM hourly_air_quality {where_clause} ORDER BY timestamp DESC LIMIT 1"
    latest_df = load_data(query_latest)
    
    if not latest_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        latest = latest_df.iloc[0]
        
        col1.metric("Current AQI", f"{latest.get('aqi', 'N/A'):.1f}", delta=latest.get('aqi_category', ''))
        col2.metric("PM2.5", f"{latest.get('pm25', 'N/A'):.1f}")
        col3.metric("PM10", f"{latest.get('pm10', 'N/A'):.1f}")
        
        pollutants = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
        vals = {p: latest.get(p, 0) for p in pollutants if pd.notna(latest.get(p))}
        worst = max(vals, key=vals.get) if vals else "N/A"
        col4.metric("Worst Pollutant", worst.upper())
    else:
        st.info("No data available in database.")
        
    st.subheader("AQI Category Distribution")
    dist_query = f"SELECT aqi_category, count(*) as count FROM hourly_air_quality {where_clause} GROUP BY aqi_category"
    dist_df = load_data(dist_query)
    if not dist_df.empty:
        fig = px.pie(dist_df, names='aqi_category', values='count', title="Historical Category Distribution")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Pollution Trends")
    where_clause = f"WHERE city = '{city}'"
    if station != "All":
        where_clause = f"WHERE station = '{station}' AND city = '{city}'"
        
    trend_query = f"SELECT timestamp, aqi, pm25, pm10 FROM hourly_air_quality {where_clause} ORDER BY timestamp DESC LIMIT 500"
    trend_df = load_data(trend_query)
    
    if not trend_df.empty:
        trend_df = trend_df.sort_values('timestamp')
        fig = px.line(trend_df, x='timestamp', y=['aqi', 'pm25', 'pm10'], title="AQI & Particulate Matter Trend")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Predict Next-Day AQI")
    st.markdown("Enter features to predict AQI.")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            temperature = st.number_input("Temperature (°C)", value=25.0)
            humidity = st.number_input("Humidity (%)", value=60.0)
            wind_speed = st.number_input("Wind Speed (km/h)", value=10.0)
            pm25 = st.number_input("PM2.5", value=40.0)
            pm10 = st.number_input("PM10", value=80.0)
        with col2:
            no2 = st.number_input("NO2", value=20.0)
            so2 = st.number_input("SO2", value=10.0)
            co = st.number_input("CO", value=0.5)
            o3 = st.number_input("O3", value=30.0)
            aqi_lag = st.number_input("Yesterday's AQI", value=100.0)
            
        submitted = st.form_submit_button("Predict")
        
    if submitted:
        payload = {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "pm25": pm25,
            "pm10": pm10,
            "no2": no2,
            "so2": so2,
            "co": co,
            "o3": o3,
            "aqi_lag_1": aqi_lag,
            "aqi_lag_2": aqi_lag,
            "aqi_lag_3": aqi_lag,
            "aqi_rolling_mean_7": aqi_lag
        }
        
        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Predicted AQI: **{result.get('predicted_aqi', 0):.2f}**")
                st.info(f"Category: **{result.get('predicted_category', 'Unknown')}**")
            else:
                st.error(f"Error from API: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to Prediction API: {e}")
