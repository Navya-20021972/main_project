@echo off
REM Backend Setup Script for Windows

echo ===== Missing Persons System - Backend Setup =====
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error creating virtual environment
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies
    exit /b 1
)

echo [4/4] Running migrations...
python manage.py migrate --noinput
python manage.py populate_sample_data

echo.
echo ===== Setup Complete! =====
echo To start the server, run:
echo   cd missing_persons_backend
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
