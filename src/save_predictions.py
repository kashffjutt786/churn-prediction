import json
import joblib
import pandas as pd
from db import get_engine, load_dataset
from features import build_features

model = joblib.load("src/model.joblib")
columns = json.load(open("src/feature_columns.json"))

df = build_features(load_dataset())
X = pd.get_dummies(df.drop(columns=["customer_id", "churn"]), drop_first=True)
X = X.reindex(columns=columns, fill_value=0)

proba = model.predict_proba(X)[:, 1]

out = pd.DataFrame({
    "customer_id": df["customer_id"],
    "churn_probability": proba.round(4),
    "risk_level": pd.cut(proba, [-0.01, 0.3, 0.6, 1.0],
                         labels=["Low", "Medium", "High"]).astype(str),
    "predicted_at": pd.Timestamp.now(),
})

out.to_sql("churn_predictions", get_engine(), schema="dbo",
           if_exists="replace", index=False)
print(f"Saved {len(out)} predictions")