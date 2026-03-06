# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (mejor para caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Default command
CMD ["python", "run_pipeline.py"]