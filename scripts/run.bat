@echo off
REM Tableau Dashboard Styler - Run Application

echo ========================================
echo Tableau Dashboard Styler
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run .\scripts\setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if main.py exists
if not exist src\main.py (
    echo WARNING: src\main.py not found yet
    echo Application entry point not created
    echo.
    echo Please create the first feature ticket to implement the application
    pause
    exit /b 1
)

REM Run the application
echo Starting Tableau Dashboard Styler...
echo.
python src\main.py

pause
