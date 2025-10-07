FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port (Render will use PORT env variable)
EXPOSE 8000

# Important: Use PORT environment variable for Render with tuned timeouts
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --timeout-keep-alive 30"]
