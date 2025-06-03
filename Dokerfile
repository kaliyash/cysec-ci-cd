# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app source code
COPY app/ app/

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python app
CMD ["python3", "app/app.py"]
