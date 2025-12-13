# Use lightweight Python
FROM python:3.11-slim

# Prevent Python from writing pyc files & unbuffer output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CLOUD_RUN=true

# Set working directory
WORKDIR /app

# Install system dependencies (needed by LightGBM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Train the model during image build
RUN python pipeline/training_pipeline.py

# Expose port for Flask
EXPOSE 5000

# Command to run Flask app
CMD ["python", "application.py"]
