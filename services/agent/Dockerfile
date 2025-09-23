FROM python:3.11-slim

# Install system dependencies for ML libraries and cryptography
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and semantic engine
COPY app.py .
COPY semantic_engine/ ./semantic_engine/
COPY shared/ ./shared/

# Expose port
EXPOSE 9000

# Start the application with PORT environment variable for Render
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-9000}"]
