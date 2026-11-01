import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mssql+pyodbc://@Kashif-PC/ChurnDB"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes&TrustServerCertificate=yes"
)

df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# TotalCharges mein kuch khali strings hain (naye customers), unhein number mein badalte hain
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

df.to_sql("raw_telco", engine, schema="dbo", if_exists="replace", index=False)
print(f"Loaded {len(df)} rows into dbo.raw_telco")