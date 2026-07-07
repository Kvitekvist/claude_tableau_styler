@echo off
REM Tableau Dashboard Styler - Development Environment Setup
REM This script prepares a clean machine for development

echo ========================================
echo Tableau Dashboard Styler - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or later from python.org
    pause
    exit /b 1
)

echo Python detected:
python --version
echo.

REM Check if virtual environment exists
if exist venv (
    echo Virtual environment already exists.
    echo.
) else (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To activate the virtual environment manually, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the application:
echo   .\scripts\run.bat
echo.
pause
