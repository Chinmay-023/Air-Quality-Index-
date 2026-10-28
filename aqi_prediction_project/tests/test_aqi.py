from src.transformation.aqi_calculation import calculate_sub_index_pm25, calculate_sub_index_pm10, get_aqi_category

def test_pm25_calculation():
    assert calculate_sub_index_pm25(15) == 25.0
    assert calculate_sub_index_pm25(45) == 75.0

def test_category():
    assert get_aqi_category(40) == 'Good'
    assert get_aqi_category(150) == 'Moderate'
    assert get_aqi_category(450) == 'Severe'
