FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY services/gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/gateway/app/ ./app/

# Copy shared modules
COPY services/shared/ ./shared/

# Expose port (Render will use PORT env variable)
EXPOSE 8000

# Important: Use PORT environment variable for Render
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
