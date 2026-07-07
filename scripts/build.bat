@echo off
REM Tableau Dashboard Styler - Build Executable

echo ========================================
echo Tableau Dashboard Styler - Build
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
    echo ERROR: src\main.py not found
    echo Cannot build executable without application entry point
    pause
    exit /b 1
)

REM Create build directory if it doesn't exist
if not exist build mkdir build

REM Create releases directory if it doesn't exist
if not exist releases mkdir releases

REM Get version from version.txt
set /p VERSION=<version.txt

echo Building Tableau Dashboard Styler v%VERSION%...
echo.

REM Run PyInstaller
pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name "TableauStyler" ^
    --distpath "releases" ^
    --workpath "build\pyinstaller" ^
    --specpath "build" ^
    src\main.py

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable created: releases\TableauStyler.exe
echo Version: %VERSION%
echo.
pause
