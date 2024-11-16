FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Make port configurable via environment variable
ENV PORT=8080

# Use gunicorn as the production server
CMD gunicorn --bind 0.0.0.0:$PORT app:app 