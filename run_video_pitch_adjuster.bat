@echo off
REM Video Pitch Adjuster GUI Launcher
REM This batch file launches the Python GUI application

echo Starting Video Pitch Adjuster GUI...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if the Python script exists
if not exist "video_pitch_adjuster.py" (
    echo ERROR: video_pitch_adjuster.py not found in current directory
    echo Please make sure you're running this from the correct folder
    pause
    exit /b 1
)

REM Check if FFMPEG is available
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFMPEG not found in PATH
    echo The application will show an error when you try to process videos
    echo Please install FFMPEG and add it to your PATH
    echo.
    echo Download from: https://ffmpeg.org/download.html
    echo.
    echo Continue anyway? Press any key to continue or Ctrl+C to exit...
    pause >nul
)

REM Launch the Python application
python video_pitch_adjuster.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)
