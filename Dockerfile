FROM python:3.12-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir --prefer-binary --default-timeout=100 -r requirements-api.txt

COPY src/features.py src/features.py
COPY src/model.joblib src/model.joblib
COPY src/feature_columns.json src/feature_columns.json
COPY api/ api/

EXPOSE 8000
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]