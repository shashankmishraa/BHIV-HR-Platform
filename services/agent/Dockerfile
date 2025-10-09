FROM python:3.12.7-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --timeout 300 --retries 3 -r requirements.txt

# Copy all application files
COPY . .

# Expose port
EXPOSE 9000

# Start the application with PORT environment variable for Render with tuned timeouts
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-9000} --timeout-keep-alive 30"]
