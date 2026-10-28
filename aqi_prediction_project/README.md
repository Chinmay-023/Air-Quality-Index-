# Air Quality Index Analysis and Prediction
End-to-End Data Engineering and MLOps Project

## 1. Project Overview
This project builds a complete end-to-end data pipeline and machine learning system to analyze and predict Air Quality Index (AQI). It implements robust data engineering principles combined with modern MLOps practices.

## 2. Problem Statement
Air pollution is a severe health hazard. Predicting the Air Quality Index (AQI) accurately allows municipalities and citizens to take preventive actions. However, raw environmental data is often messy, missing, or unstructured. This project addresses the challenge by orchestrating automated ETL pipelines, building a structured data warehouse, and deploying predictive machine learning models in a fully reproducible environment.

## 3. Objectives
- Automated Data Ingestion
- Rigorous Data Quality Checks
- Analytics Data Warehousing (PostgreSQL)
- Time-series Machine Learning Prediction
- Comprehensive Experiment Tracking (MLflow)
- Containerized API and Dashboard Deployment

## 4. Architecture
See `docs/architecture.md` for a full overview of the Data Flow and MLOps layers.

## 5. Technologies
- **Python 3.10**
- **Orchestration**: Apache Airflow
- **Database**: PostgreSQL
- **Visualization**: Streamlit, Plotly
- **Machine Learning**: Scikit-learn, MLflow
- **API Framework**: FastAPI, Uvicorn
- **Containerization**: Docker, Docker Compose
- **Testing**: Pytest

## 6. Data Sources
- **OpenAQ API**: For PM2.5, PM10, NO2, SO2, CO, O3 measurements.
- **Open-Meteo API**: For temperature, humidity, precipitation, wind metrics.

## 7. Installation & Setup
1. **Clone the repository.**
2. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and update values.
   ```bash
   cp .env.example .env
   ```

## 8. Running the Project (End-to-End Demonstration)

**Step 1: Start Services**
```bash
docker-compose up --build -d
```
This launches Postgres, Airflow, MLflow, FastAPI, and Streamlit.

**Step 2: Database Initialization**
Inside the container or via python locally, initialize tables:
```bash
python -c "from src.database.connection import init_db; init_db()"
```

**Step 3: Run Ingestion & ETL (Airflow)**
1. Navigate to `http://localhost:8080` (Airflow UI).
2. Unpause and trigger `aqi_end_to_end_pipeline`.
3. Check `data/raw/` for JSON files and `data/rejected/` for invalid records.

**Step 4: Train Machine Learning Models**
```bash
python src/models/train_regression.py
python src/models/train_classification.py
```
View experiments at MLflow (`http://localhost:5000`). The best models are automatically registered.

**Step 5: View Dashboard & Predict**
Navigate to `http://localhost:8501`. Explore Analytics, Trends, and the Prediction form (powered by FastAPI at `http://localhost:8000`).

## 9. Testing
Run tests using:
```bash
pytest tests/
```

## 10. Monitoring & Retraining
Run the monitoring script to evaluate recent predictions against actual values.
```bash
python src/monitoring/performance_monitor.py
```

## Project Limitations & Future Enhancements
- Currently models use simple time-based splits. Could be enhanced with cross-validation for time series.
- Add deep learning models (LSTMs) for complex sequence prediction.
