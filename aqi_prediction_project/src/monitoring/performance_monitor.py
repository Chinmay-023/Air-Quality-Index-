import pandas as pd
from src.database.connection import get_engine
from sklearn.metrics import mean_absolute_error
from src.utils.logger import get_logger

logger = get_logger("monitoring")

def check_model_performance(threshold_mae=20.0):
    query = """
        SELECT predicted_aqi, actual_aqi
        FROM model_predictions
        WHERE actual_aqi IS NOT NULL
        ORDER BY prediction_timestamp DESC
        LIMIT 100
    """
    try:
        engine = get_engine()
        df = pd.read_sql(query, engine)
        
        if df.empty or len(df) < 10:
            logger.info("Not enough data to calculate performance metrics.")
            return
            
        mae = mean_absolute_error(df['actual_aqi'], df['predicted_aqi'])
        logger.info(f"Recent MAE over last {len(df)} predictions: {mae:.2f}")
        
        if mae > threshold_mae:
            logger.warning(f"ALERT: MAE ({mae:.2f}) exceeded threshold ({threshold_mae}). Retraining needed!")
    except Exception as e:
        logger.error(f"Error checking model performance: {e}")

if __name__ == "__main__":
    check_model_performance()
