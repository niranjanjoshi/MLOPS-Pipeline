from fastapi import FastAPI, Response, HTTPException
import pandas as pd
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, Histogram
from src.model import load_model
import os
import sqlite3
from datetime import datetime
import json
import time
from pydantic import BaseModel
import subprocess


app = FastAPI()

PREDICTION_COUNTER = Counter("prediction_requests_total", "Total prediction requests")
PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds", "Prediction request latency in seconds"
)

# Initialize SQLite DB and table (run once at startup)
conn = sqlite3.connect("prediction_logs.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS prediction_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    input_json TEXT,
    prediction REAL
)
"""
)
conn.commit()


predict_counter = Counter("predict_requests", "Number of prediction requests")


class HousingFeatures(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


FEATURE_ORDER = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]


@app.post("/predict")
def predict(input_data: HousingFeatures):
    model_path = "models/BestHousingModel.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            "Model file not found. Train the model first using `train.py`."
        )
    model = load_model(model_path)
    PREDICTION_COUNTER.inc()
    start_time = time.time()

    # Convert Pydantic model to dict and reorder columns
    data_dict = input_data.dict()
    df = pd.DataFrame(
        [[data_dict[col] for col in FEATURE_ORDER]], columns=FEATURE_ORDER
    )

    predict_counter.inc()
    prediction = model.predict(df)[0]

    latency = time.time() - start_time
    PREDICTION_LATENCY.observe(latency)

    cursor.execute(
        "INSERT INTO prediction_logs (timestamp, input_json, prediction) VALUES (?, ?, ?)",
        (datetime.utcnow().isoformat(), json.dumps(data_dict), prediction),
    )
    conn.commit()

    return {"prediction": prediction}


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/retrain")
def retrain():
    try:
        # Run train.py using the same python executable
        result = subprocess.run(
            ["python", "src/train.py"],
            capture_output=True,
            text=True,
            check=True,
        )
        return {
            "message": "Training completed successfully.",
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {e.stderr}")
