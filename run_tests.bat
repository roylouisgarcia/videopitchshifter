@echo off
REM Test Runner for Video Pitch Adjuster
REM This batch file runs all available tests

echo Running Video Pitch Adjuster Tests...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher from https://python.org
    pause
    exit /b 1
)

echo Testing FFMPEG pitch adjustment methods...
python tests\test_pitch_methods.py
echo.

echo Testing button and file functionality...
python tests\test_functionality.py
echo.

echo Testing dynamic filename generation...
python tests\test_filename_generation.py
echo.

echo All tests completed!
pause
