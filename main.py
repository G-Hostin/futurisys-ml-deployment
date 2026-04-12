from fastapi import FastAPI, Depends
import joblib
from sqlalchemy.orm import Session
from app.schemas import EmployeeInput, PredictionOutput
from app.preprocessing import preprocess_input
from db.database import engine, SessionLocal, Base
from db.models import PredictionInput, PredictionOutput as PredictionOutputDB

Base.metadata.create_all(engine)

app = FastAPI(
    title="Futurisys ML API",
    description="API de prediction d'attrition des employes",
    version="0.1.0",
)

model = joblib.load("model/model_xgb.joblib")
THRESHOLD = 0.545


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Futurisys ML API is running"}


@app.post("/predict", response_model=PredictionOutput)
def predict(employee: EmployeeInput, db: Session = Depends(get_db)):
    df = preprocess_input(employee.model_dump())
    proba = model.predict_proba(df)[:, 1][0]
    prediction = int(proba >= THRESHOLD)

    if proba < 0.3:
        risk_level = "faible"
    elif proba < THRESHOLD:
        risk_level = "modéré"
    else:
        risk_level = "élevé"

    # enregistrer l'input en base
    db_input = PredictionInput(**employee.model_dump())
    db.add(db_input)
    db.commit()
    db.refresh(db_input)

    # enregistrer l'output en base
    db_output = PredictionOutputDB(
        input_id=db_input.id,
        prediction=prediction,
        probability=round(float(proba), 3),
        risk_level=risk_level,
    )
    db.add(db_output)
    db.commit()

    return PredictionOutput(
        prediction=prediction,
        probability=round(float(proba), 3),
        risk_level=risk_level,
    )