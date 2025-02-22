# Use an official lightweight Python image.
FROM python:3.12-slim

# Set environment variables to disable buffering.
ENV PYTHONUNBUFFERED=1
ENV PORT=8501

# Install system dependencies required for building Python packages.
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory.
WORKDIR /app

# Copy requirements.txt into the container.
COPY requirements.txt /app/requirements.txt

# Upgrade pip, setuptools, and wheel to the latest versions, then install Python dependencies.
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy the rest of the application code into the container.
COPY . /app

# Expose the port that Streamlit uses.
EXPOSE 8501

# Set the command to run the Streamlit app.
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false"]
