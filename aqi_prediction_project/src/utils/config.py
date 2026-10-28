import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent.parent

def load_config() -> dict:
    """Load configuration from config.yaml"""
    config_path = get_project_root() / "config" / "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

# Global config instance
CONFIG = load_config()

# Database
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "aqi_db")
DB_USER = os.getenv("POSTGRES_USER", "aqi_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "aqi_password")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# OpenAQ
OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY", "")

# API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
