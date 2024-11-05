# Use the official Python slim image as the base
FROM python:3.11-slim

# Install system dependencies required by Playwright and Chromium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080  

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright 1.37.0 and download browsers
RUN pip install playwright==1.37.0
RUN playwright install --with-deps

# Copy the rest of the application code into the container
COPY . .

# Expose the port (optional, Cloud Run handles it)
EXPOSE 8080

# Define the default command to run the application
CMD gunicorn main:app --bind 0.0.0.0:$PORT --workers 3 --timeout 120