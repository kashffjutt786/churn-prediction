import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src"))
from features import build_features  # noqa: E402

model = joblib.load(ROOT / "src" / "model.joblib")
columns = json.load(open(ROOT / "src" / "feature_columns.json"))

app = FastAPI(title="Churn Prediction API", version="1.0")


class Customer(BaseModel):
    gender: str = "Female"
    senior_citizen: int = 0
    partner: str = "Yes"
    dependents: str = "No"
    tenure_months: int = 5
    phone_service: str = "Yes"
    multiple_lines: str = "No"
    internet_service: str = "Fiber optic"
    online_security: str = "No"
    online_backup: str = "No"
    device_protection: str = "No"
    tech_support: str = "No"
    streaming_tv: str = "Yes"
    streaming_movies: str = "Yes"
    contract: str = "Month-to-month"
    paperless_billing: str = "Yes"
    payment_method: str = "Electronic check"
    monthly_charges: float = 85.5
    total_charges: float = 420.0


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(customer: Customer):
    df = build_features(pd.DataFrame([customer.model_dump()]))
    # Single row par drop_first=True galat hota hai, is liye False,
    # phir training wale columns ke mutabiq reindex
    X = pd.get_dummies(df, drop_first=False).reindex(columns=columns, fill_value=0)

    prob = float(model.predict_proba(X)[0, 1])
    risk = "Low" if prob <= 0.3 else "Medium" if prob <= 0.6 else "High"
    return {"churn_probability": round(prob, 4), "risk_level": risk}