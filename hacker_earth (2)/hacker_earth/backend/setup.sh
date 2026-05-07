#!/bin/bash
# Setup script for NyayaMitra Backend

echo "=========================================="
echo "    NyayaMitra Backend Setup Script"
echo "=========================================="

echo "[1/4] Creating virtual environment (venv)..."
python -m venv venv

# Platform independent activation check
if [ -f "venv/Scripts/activate" ]; then
    # Windows
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    # Linux/Mac
    source venv/bin/activate
else
    echo "Failed to find activation script. Please activate venv manually."
    exit 1
fi

echo "[2/4] Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[3/4] Downloading spaCy English model..."
python -m spacy download en_core_web_sm

echo "[4/4] Creating necessary directories..."
mkdir -p outputs
mkdir -p uploads

echo "=========================================="
echo "Setup complete!"
echo "To run the server:"
echo "1. Activate venv: source venv/Scripts/activate (Windows) or source venv/bin/activate (Linux/Mac)"
echo "2. Start server: uvicorn app:app --reload --host 0.0.0.0 --port 8000"
echo "=========================================="
