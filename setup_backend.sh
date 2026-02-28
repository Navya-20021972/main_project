#!/bin/bash
# Backend Setup Script for Linux/Mac

echo "===== Missing Persons System - Backend Setup ====="
echo ""

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error creating virtual environment"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo "[3/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

echo "[4/4] Running migrations..."
python manage.py migrate --noinput
python manage.py populate_sample_data

echo ""
echo "===== Setup Complete! ====="
echo "To start the server, run:"
echo "  cd missing_persons_backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
