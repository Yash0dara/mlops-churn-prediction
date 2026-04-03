FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-production.txt .

# Install lightweight packages first
RUN pip install --no-cache-dir --timeout 300 -r requirements-production.txt

# Install xgboost separately with retries
RUN pip install --no-cache-dir --timeout 600 --retries 5 xgboost

# Copy application code
COPY src/ ./src/
COPY models/ ./models/
COPY configs/ ./configs/

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]