import joblib
import pandas as pd

def load_model(path="models/ridge_model.pkl"):
    return joblib.load(path)

def predict(model, input_data: dict):
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)
    return prediction[0]
