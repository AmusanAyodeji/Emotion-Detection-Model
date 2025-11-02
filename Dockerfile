# Use a lightweight Python image
FROM python:3.10-slim

# Install system dependencies (this fixes the libGL.so.1 issue)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (Railway expects this)
ENV PORT=8000
EXPOSE 8000

# Run your app (update filename if different)
CMD ["python", "api.py"]
