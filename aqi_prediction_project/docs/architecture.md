# System Architecture

## Data Flow Layer
1. **Source Layer**: Data is collected from OpenAQ API (Pollution) and Open-Meteo API (Weather).
2. **Ingestion Layer**: Python collectors (`src/ingestion/`) hit APIs and retrieve JSON.
3. **Raw Layer**: Responses are saved as timestamped JSON files in `data/raw/`.
4. **Staging Layer**: Raw JSON is parsed into DataFrames (`src/transformation/cleaning.py`).
5. **Validation Layer**: Data quality checks are enforced. Invalid records move to `data/rejected/`.
6. **Cleaned Layer**: Valid records are aggregated hourly and AQI is calculated.
7. **PostgreSQL**: Structured data is loaded into `hourly_air_quality`, `hourly_weather`, `stations`.
8. **Analytics Layer**: SQL Views like `daily_air_quality` prepare aggregated metrics.
9. **Dashboard Layer**: Streamlit reads from DB to display visual metrics.

## MLOps Pipeline Layer
1. **Feature Engineering**: Queries PostgreSQL, handles missing values, and builds lags/rolling features.
2. **Model Training**: Regression & Classification models are trained using a chronological train/val/test split.
3. **MLflow Tracking**: Hyperparameters, metrics (MAE, RMSE, F1), and model artifacts are tracked.
4. **Model Registry**: The best-performing model is registered in MLflow.
5. **FastAPI**: Exposes a prediction endpoint that loads the registered model.
6. **Docker**: Orchestrates Postgres, Airflow, MLflow, FastAPI, and Streamlit via `docker-compose`.
7. **Monitoring**: Evaluates actual vs predicted AQI and checks for drift/MAE threshold limits.
8. **Retraining**: Scheduled scripts flag when performance degrades below set thresholds.
