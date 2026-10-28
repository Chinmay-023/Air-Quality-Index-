import os
import logging
import logging.config
import yaml
from pathlib import Path
from src.utils.config import get_project_root

def setup_logging():
    """Setup logging configuration"""
    config_path = get_project_root() / "config" / "logging.yaml"
    
    # Ensure logs directory exists
    log_dir = get_project_root() / "logs"
    log_dir.mkdir(exist_ok=True)
    
    if config_path.exists():
        with open(config_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

def get_logger(name="aqi_pipeline"):
    setup_logging()
    return logging.getLogger(name)
