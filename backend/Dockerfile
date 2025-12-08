# Backend Dockerfile - FastAPI with Python
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create database directory (for SQLite persistence)
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Run database seed and start server
CMD ["sh", "-c", "python seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

