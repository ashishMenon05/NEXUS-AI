@echo off
echo ==============================================================
echo NEXUS Incident Investigation Environment Setup
echo ==============================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b
)

REM Check npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js/npm is not installed or not in PATH!
    pause
    exit /b
)

echo [1/3] Setting up Backend Virtual Environment...
python -m venv backend\venv
call backend\venv\Scripts\activate.bat
pip install -r backend\requirements.txt

echo.
echo [2/3] Setting up Frontend Dependencies...
cd frontend
call npm install
cd ..

echo.
echo [3/3] Validating OpenEnv Compliance...
call backend\venv\Scripts\python.exe openenv_validator.py

echo.
echo ==============================================================
echo SETUP COMPLETE!
echo.
echo To run locally without Docker:
echo 1. Start UI:    cd frontend ^& npm run dev
echo 2. Start API:   cd backend ^& venv\Scripts\uvicorn main:app --reload
echo ==============================================================
pause
