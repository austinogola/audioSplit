FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg wget && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .
COPY runtime.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install  -r requirements.txt
# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Start app with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
