from db import get_engine
import pandas as pd

df = pd.read_sql(
    "SELECT p.customer_id, p.churn_probability, p.risk_level, "
    "b.contract, b.monthly_charges "
    "FROM dbo.churn_predictions p "
    "JOIN dbo.billing b ON b.customer_id = p.customer_id", get_engine())
df.to_csv("data/predictions_snapshot.csv", index=False)
print(len(df), "rows exported")