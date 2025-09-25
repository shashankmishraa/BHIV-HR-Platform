FROM python:3.11-slim

# Install system dependencies for cryptography
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .
# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Copy shared modules
COPY shared/ ./shared/

# Set PYTHONPATH to recognize app as root package
ENV PYTHONPATH=/app

# Expose port (Render will use PORT env variable)
EXPOSE 8000

# Important: Use PORT environment variable for Render
# Run with proper module context
CMD ["sh", "-c", "cd /app && python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
