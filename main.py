from fastapi import FastAPI
import joblib
import numpy as np
from app.schemas import EmployeeInput, PredictionOutput
from app.preprocessing import preprocess_input

app = FastAPI(
    title="Futurisys ML API",
    description="API de prediction d'attrition des employes",
    version="0.1.0",
)

model = joblib.load("model/model_xgb.joblib")
THRESHOLD = 0.545


@app.get("/")
def root():
    return {"message": "Futurisys ML API is running"}


@app.post("/predict", response_model=PredictionOutput)
def predict(employee: EmployeeInput):
    df = preprocess_input(employee.model_dump()) # converti l'objet Pydantic en dictionnaire python pour le passer au preprocess
    proba = model.predict_proba(df)[:, 1][0]
    prediction = int(proba >= THRESHOLD)

    if proba < 0.3:
        risk_level = "faible"
    elif proba < THRESHOLD:
        risk_level = "modéré"
    else:
        risk_level = "élevé"

    return PredictionOutput(
        prediction=prediction,
        probability=round(float(proba), 3),
        risk_level=risk_level,
    )