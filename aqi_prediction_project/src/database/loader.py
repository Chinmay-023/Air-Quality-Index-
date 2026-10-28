import pandas as pd
from sqlalchemy import create_engine
from src.database.connection import get_engine
from src.utils.logger import get_logger

logger = get_logger("loader")

def load_dataframe_to_postgres(df: pd.DataFrame, table_name: str, if_exists: str = 'append'):
    if df.empty:
        logger.info(f"Empty dataframe, skipping load to {table_name}.")
        return
        
    engine = get_engine()
    
    try:
        # Pandas to_sql with if_exists='append' will fail if there are unique constraint violations.
        # To make it more robust for our pipeline, we can insert row by row, or write a custom insert on conflict.
        # For simplicity, we use to_sql and catch IntegrityError.
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        logger.info(f"Loaded {len(df)} rows into {table_name}")
    except Exception as e:
        logger.error(f"Failed to load data into {table_name}: {e}")
