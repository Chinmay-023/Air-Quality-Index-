from sqlalchemy import create_engine
from src.utils.config import DB_URL
from src.utils.logger import get_logger

logger = get_logger("database")

def get_engine():
    try:
        engine = create_engine(DB_URL)
        return engine
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise e

def init_db():
    from src.utils.config import get_project_root
    engine = get_engine()
    schema_path = get_project_root() / "src" / "database" / "schema.sql"
    
    with open(schema_path, "r") as f:
        schema = f.read()
        
    with engine.begin() as conn:
        from sqlalchemy import text
        conn.execute(text(schema))
    logger.info("Database schema initialized.")
