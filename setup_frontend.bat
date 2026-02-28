@echo off
REM Frontend Setup Script for Windows

echo ===== Missing Persons System - Frontend Setup =====
echo.

echo [1/3] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js not found. Please install Node.js from https://nodejs.org/
    exit /b 1
)

echo [2/3] Installing dependencies...
npm install
if %errorlevel% neq 0 (
    echo Error installing dependencies
    exit /b 1
)

echo [3/3] Creating .env file...
echo REACT_APP_API_URL=http://localhost:8000/api > .env

echo.
echo ===== Setup Complete! =====
echo To start the development server, run:
echo   cd missing_persons_frontend
echo   npm start
echo.
echo The app will open at http://localhost:3000
echo.
