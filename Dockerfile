# Use a base image with Python
FROM python:3.10-slim

# Install dependencies including Chrome
RUN apt-get update && \
    apt-get install -y wget unzip gnupg curl ca-certificates \
    chromium chromium-driver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set Chrome paths for Railway
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for web access
EXPOSE $PORT

# Start the Flask app
CMD ["python", "app.py"]
