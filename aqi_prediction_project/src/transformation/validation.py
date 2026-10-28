import pandas as pd
import datetime
from src.utils.logger import get_logger
from src.utils.config import get_project_root

logger = get_logger("validation")

def validate_openaq_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Validate OpenAQ data and return (valid_df, rejected_df)."""
    if df.empty:
        return df, pd.DataFrame()
        
    df = df.copy()
    rejected_list = []
    
    null_mask = df['timestamp'].isnull() | df['station'].isnull() | df['pollutant'].isnull()
    if null_mask.any():
        rej = df[null_mask].copy()
        rej['reject_reason'] = "Null critical fields (timestamp, station, or pollutant)"
        rejected_list.append(rej)
        
    neg_mask = (~null_mask) & (df['value'] < 0)
    if neg_mask.any():
        rej = df[neg_mask].copy()
        rej['reject_reason'] = "Negative pollutant value"
        rejected_list.append(rej)
        
    valid_mask = (~null_mask) & (~neg_mask)
    valid_df = df[valid_mask].copy()
    
    if not valid_df.empty:
        dup_mask = valid_df.duplicated(subset=['timestamp', 'station', 'pollutant'], keep='first')
        if dup_mask.any():
            rej = valid_df[dup_mask].copy()
            rej['reject_reason'] = "Duplicate record"
            rejected_list.append(rej)
            valid_df = valid_df[~dup_mask].copy()
            
    rejected_df = pd.concat(rejected_list) if rejected_list else pd.DataFrame()
    logger.info(f"OpenAQ Validation: {len(valid_df)} valid, {len(rejected_df)} rejected.")
    return valid_df, rejected_df

def save_rejected(df: pd.DataFrame, source: str):
    """Save rejected records to the rejected directory."""
    if df.empty:
        return
        
    rej_dir = get_project_root() / "data" / "rejected"
    rej_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = rej_dir / f"{source}_rejected_{timestamp}.csv"
    
    df['reject_timestamp'] = pd.Timestamp.utcnow()
    df.to_csv(filepath, index=False)
    logger.info(f"Saved {len(df)} rejected {source} records to {filepath}")
