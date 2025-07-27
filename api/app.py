from fastapi import FastAPI, Response
import pandas as pd
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from src.model import load_model
import os
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

model_path = "models/ridge_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError("Model file not found. Train the model first using `train.py`.")

model = load_model(model_path)
predict_counter = Counter("predict_requests", "Number of prediction requests")

@app.post("/predict")
def predict(input_data: dict):
    df = pd.DataFrame([input_data])
    predict_counter.inc()
    prediction = model.predict(df)[0]
    return {"prediction": prediction}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)