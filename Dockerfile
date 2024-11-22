FROM python:3.9-slim

WORKDIR /app

# Clean and update apt
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update

# Install system dependencies
RUN apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-dev \
    build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip wheel setuptools && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080

# Start the application
CMD gunicorn --bind 0.0.0.0:$PORT app:app