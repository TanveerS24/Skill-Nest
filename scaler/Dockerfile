FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    docker.io \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scaler code
COPY scaler.py .
COPY templates/ ./templates/

# Create directory for Nginx configs
RUN mkdir -p /etc/nginx/conf.d

# Expose Flask API port
EXPOSE 9090

# Run the scaler
CMD ["python", "scaler.py"]
