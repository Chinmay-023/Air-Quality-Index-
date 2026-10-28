import pandas as pd
from src.transformation.validation import validate_openaq_data

def test_validate_openaq_data():
    data = {
        'timestamp': ['2023-01-01T00:00:00Z', None, '2023-01-01T01:00:00Z', '2023-01-01T02:00:00Z'],
        'station': ['st1', 'st1', None, 'st2'],
        'pollutant': ['pm25', 'pm10', 'pm25', 'pm25'],
        'value': [15.0, 20.0, 30.0, -5.0]
    }
    df = pd.DataFrame(data)
    valid, rejected = validate_openaq_data(df)
    
    assert len(valid) == 1
    assert valid.iloc[0]['value'] == 15.0
    assert len(rejected) == 3
