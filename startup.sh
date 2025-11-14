#!/bin/bash
# startup.sh - Install deps, download dataset, then start API

# Exit on any error
set -e

echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Downloading latest dataset..."
python scripts/update_dataset.py

echo "Starting API..."
exec uvicorn src.main:app --host 0.0.0.0 --port $PORT