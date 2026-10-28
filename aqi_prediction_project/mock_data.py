import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.database.connection import get_engine
from src.database.loader import load_dataframe_to_postgres

def generate_mock_data():
    engine = get_engine()
    dates = pd.date_range(end=datetime.utcnow(), periods=24*30, freq='H')
    
    np.random.seed(42)
    data = []
    
    locations = {
        'Bengaluru': ['BTM Layout', 'Peenya', 'Hebbal', 'Banshankari', 'AECS Layout', 'KR Puram', 'Whitefield', 'Indiranagar', 'Jayanagar', 'Koramangala'],
        'Delhi': ['Anand Vihar', 'RK Puram', 'Punjabi Bagh', 'ITO', 'Okhla', 'Dwarka', 'Rohini', 'Vasant Kunj', 'Lajpat Nagar', 'Karol Bagh'],
        'Mumbai': ['Bandra', 'Colaba', 'Andheri', 'Borivali', 'Dadar', 'Juhu', 'Powai', 'Malad', 'Goregaon', 'Kurla'],
        'Chennai': ['Adyar', 'Velachery', 'Guindy', 'T Nagar', 'Mylapore', 'Anna Nagar', 'OMR', 'Tambaram', 'Alwarpet', 'Nungambakkam'],
        'Kolkata': ['Salt Lake', 'Ballygunge', 'Jadavpur', 'Park Street', 'New Town', 'Howrah', 'Behala', 'Dum Dum', 'Alipore', 'Rajarhat'],
        'Hyderabad': ['Banjara Hills', 'Gachibowli', 'Kukatpally', 'HITEC City', 'Jubilee Hills', 'Secunderabad', 'Ameerpet', 'Madhapur', 'Kondapur', 'Begumpet'],
        'Pune': ['Kothrud', 'Hinjewadi', 'Viman Nagar', 'Baner', 'Koregaon Park', 'Magarpatta', 'Wakad', 'Shivaji Nagar', 'Kalyani Nagar', 'Hadapsar'],
        'Ahmedabad': ['Navrangpura', 'Maninagar', 'Satellite', 'Bopal', 'Vastrapur', 'Thaltej', 'Prahlad Nagar', 'SG Highway', 'Ashram Road', 'Paldi'],
        'Surat': ['Adajan', 'Vesu', 'Piplod', 'Varachha', 'Rander', 'Katargam', 'Udhna', 'Athwalines', 'City Light', 'Pal'],
        'Jaipur': ['Malviya Nagar', 'Vaishali Nagar', 'Mansarovar', 'Bani Park', 'C Scheme', 'Tonk Road', 'Raja Park', 'Jagatpura', 'Vidyadhar Nagar', 'Jhotwara'],
        'Kanpur': ['Kakadeo', 'Swaroop Nagar', 'Kidwai Nagar', 'Civil Lines', 'Kalyanpur', 'PPN Market', 'Fazalganj', 'Govind Nagar', 'Barra', 'Shyam Nagar'],
        'Lucknow': ['Gomti Nagar', 'Aliganj', 'Indira Nagar', 'Hazratganj', 'Aminabad', 'Mahanagar', 'Ashiyana', 'Vikas Nagar', 'Kapoorthala', 'Chowk'],
        'Nagpur': ['Dharampeth', 'Mahal', 'Sitabuldi', 'Sadar', 'Wardhaman Nagar', 'Itwari', 'Ramdaspeth', 'Manish Nagar', 'Pratap Nagar', 'Hingna'],
        'Indore': ['Palasia', 'Vijay Nagar', 'Rajwada', 'Bhawarkuan', 'MG Road', 'AB Road', 'Annapurna', 'Sudama Nagar', 'Saket Nagar', 'LIG Colony'],
        'Patna': ['Kankarbagh', 'Rajendra Nagar', 'Boring Road', 'Patliputra Colony', 'Fraser Road', 'Gandhi Maidan', 'Anisabad', 'Danapur', 'Phulwari Sharif', 'Kumhrar'],
        'Bhopal': ['Arera Colony', 'MP Nagar', 'Bairagarh', 'Kolar Road', 'Indrapuri', 'TT Nagar', 'Awadhpuri', 'Habibganj', 'Govindpura', 'Shyamla Hills'],
        'Vadodara': ['Alkapuri', 'Karelibaug', 'Sama', 'Akota', 'Fatehgunj', 'Gotri', 'Manjalpur', 'Makarpura', 'Sayajigunj', 'Waghodia'],
        'Agra': ['Tajganj', 'Sanjay Place', 'Kamla Nagar', 'Dayal Bagh', 'Sadar Bazar', 'Sikandra', 'Shahganj', 'Khandari', 'Rakabganj', 'Fatehabad Road'],
        'Varanasi': ['Lanka', 'Sigra', 'Cantt', 'Bhelupur', 'Mahmoorganj', 'Godowlia', 'Assi Ghat', 'Sarnath', 'Ramnagar', 'Shivpur'],
        'Madurai': ['Anna Nagar (Madurai)', 'KK Nagar', 'SS Colony', 'Tallakulam', 'Bypass Road', 'Tirunagar', 'Mattuthavani', 'Sellur', 'Palanganatham', 'Villapuram'],
        'Coimbatore': ['RS Puram', 'Peelamedu', 'Gandhipuram', 'Saravanampatti', 'Sai Baba Colony', 'Vadavalli', 'Ramanathapuram', 'Race Course', 'Singanallur', 'Kuniyamuthur'],
        'Kochi': ['Edappally', 'Kaloor', 'Fort Kochi', 'Marine Drive', 'Vyttila', 'Kakkanad', 'Palarivattom', 'Panampilly Nagar', 'MG Road (Kochi)', 'Aluva'],
        'Visakhapatnam': ['MVP Colony', 'Gajuwaka', 'Siripuram', 'Madhurawada', 'Dwaraka Nagar', 'NAD X Road', 'Seethammadhara', 'Akkayyapalem', 'RK Beach', 'Rushikonda'],
        'Chandigarh': ['Sector 17', 'Sector 35', 'Sector 43', 'Sector 22', 'Sector 15', 'Sector 8', 'Sector 19', 'Manimajra', 'Industrial Area', 'IT Park'],
        'Mysore': ['Saraswathipuram', 'Kuvempunagar', 'Gokulam', 'Jayalakshmipuram', 'Vijayanagar', 'VV Mohalla', 'Siddarthanagar', 'JP Nagar', 'Bannimantap', 'Hebbal (Mysore)']
    }
    
    # Add import at the top (conceptually) or just implement wide bounds
    from src.transformation.aqi_calculation import calculate_sub_index_pm25, calculate_sub_index_pm10, get_aqi_category

    # Pre-calculate a daily baseline for every station to avoid the Central Limit Theorem smoothing effect!
    daily_severities = {}
    unique_dates = np.unique([d.date() for d in dates])
    
    for ud in unique_dates:
        for city, stations_list in locations.items():
            for s in stations_list:
                # Assign realistic pollution bounds based on the city!
                if city in ['Delhi', 'Kanpur', 'Patna', 'Lucknow', 'Agra']:
                    # Highly polluted cities (to train Severe/Very Poor)
                    base_pm25 = np.random.uniform(150, 450)
                elif city in ['Mumbai', 'Kolkata', 'Hyderabad', 'Ahmedabad', 'Surat']:
                    # Medium polluted cities (to train Poor/Moderate)
                    base_pm25 = np.random.uniform(60, 200)
                else:
                    # Clean/Coastal cities like Bangalore, Chennai, Mysore (to train Good/Satisfactory)
                    base_pm25 = np.random.uniform(5, 80)
                    
                # PM10 MUST BE GREATER THAN PM2.5 IN REAL LIFE!
                base_pm10 = base_pm25 + np.random.uniform(10, 150)
                daily_severities[(s, ud)] = (base_pm25, base_pm10)

    for d in dates:
        date_key = d.date()
        for city, stations_list in locations.items():
            for station in stations_list:
                daily_pm25, daily_pm10 = daily_severities[(station, date_key)]
                
                # Apply small hourly fluctuations (±20%) to the daily baseline
                pm25 = max(5, daily_pm25 * np.random.uniform(0.8, 1.2))
                # Ensure PM10 remains physically valid after noise
                pm10 = max(pm25 + 5, daily_pm10 * np.random.uniform(0.8, 1.2))
                
                aqi = max(calculate_sub_index_pm25(pm25), calculate_sub_index_pm10(pm10))
                category = get_aqi_category(aqi)
                
                data.append({
                    'timestamp': d,
                    'station': station,
                    'city': city,
                    'pm25': pm25,
                    'pm10': pm10,
                    'aqi': aqi,
                    'aqi_category': category
                })
            
    df = pd.DataFrame(data)
    with engine.begin() as conn:
        conn.execute("TRUNCATE TABLE hourly_air_quality CASCADE;")
        conn.execute("TRUNCATE TABLE stations CASCADE;")
    load_dataframe_to_postgres(df, 'hourly_air_quality', if_exists='append')
    
    stations_data = []
    for city, stations_list in locations.items():
        for s in stations_list:
            stations_data.append({'name': s, 'city': city})
            
    stations_df = pd.DataFrame(stations_data)
    load_dataframe_to_postgres(stations_df, 'stations', if_exists='append')
    print("Mock data generated and loaded to DB.")

if __name__ == "__main__":
    generate_mock_data()
