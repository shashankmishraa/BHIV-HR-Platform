FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and semantic engine
COPY app.py .
COPY semantic_engine/ ./semantic_engine/
COPY shared/ ./shared/

# Expose port
EXPOSE 9000

# Start the application with PORT environment variable for Render
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-9000}"]
