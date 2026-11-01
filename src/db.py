import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    return create_engine(
        "mssql+pyodbc://@Kashif-PC/ChurnDB"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&trusted_connection=yes&TrustServerCertificate=yes"
    )

def load_dataset():
    query = "SELECT * FROM dbo.vw_churn_dataset"
    return pd.read_sql(query, get_engine())