from sqlalchemy import create_engine, text

engine = create_engine(
    "mssql+pyodbc://@Kashif-PC/master"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes&TrustServerCertificate=yes"
)

with engine.connect() as conn:
    print(conn.execute(text("SELECT @@VERSION")).scalar())