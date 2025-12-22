@echo off
title Dynamic Island - Setup
color 0A
cd /d "%~dp0"

echo.
echo ================================================================
echo    DYNAMIC ISLAND SPOTIFY CONTROLLER - SETUP
echo ================================================================
echo.

REM Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
echo Python found!
echo.

REM Create venv if not exists
echo [2/4] Setting up virtual environment...
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
echo Virtual environment ready!
echo.

REM Install packages
echo [3/4] Installing packages (please wait)...
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo Packages installed!
echo.

REM Check/Create .env
if exist .env (
    echo [4/4] API config found!
    goto :run_app
)

echo [4/4] Setting up Spotify API...
echo.
echo ================================================================
echo    You need Spotify API credentials to use this app.
echo    
echo    1. Go to: https://developer.spotify.com/dashboard
echo    2. Login and click "Create App"
echo    3. App name: Dynamic Island
echo    4. Redirect URI: http://localhost:8888/callback
echo    5. Check "Web API" and Save
echo    6. Click Settings and copy Client ID + Secret
echo ================================================================
echo.

set /p CLIENT_ID="Enter Client ID: "
if "%CLIENT_ID%"=="" (
    echo Client ID cannot be empty!
    pause
    exit /b 1
)

set /p CLIENT_SECRET="Enter Client Secret: "
if "%CLIENT_SECRET%"=="" (
    echo Client Secret cannot be empty!
    pause
    exit /b 1
)

echo SPOTIPY_CLIENT_ID=%CLIENT_ID%> .env
echo SPOTIPY_CLIENT_SECRET=%CLIENT_SECRET%>> .env
echo SPOTIPY_REDIRECT_URI=http://localhost:8888/callback>> .env

echo.
echo API credentials saved!
echo.

:run_app
echo ================================================================
echo    SETUP COMPLETE! Starting Dynamic Island...
echo ================================================================
echo.
echo The app will run in background. You can close this window.
echo To exit: Right-click tray icon (bottom-right) and click Exit
echo.

REM Run app in background using pythonw (no console)
start "" venv\Scripts\pythonw.exe dynamic_island.py

echo App started! You can close this window now.
pause
