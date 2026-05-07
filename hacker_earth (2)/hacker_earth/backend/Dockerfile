FROM python:3.9-slim

# Install system dependencies required for OpenCV, PyMuPDF, and PaddleOCR
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model during build to speed up runtime
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
