@echo off
title Dynamic Island
cd /d "%~dp0"

echo.
echo ================================================================
echo    DYNAMIC ISLAND SPOTIFY CONTROLLER
echo ================================================================
echo.

REM Check setup
if not exist venv (
    echo ERROR: Setup not completed!
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

if not exist .env (
    echo ERROR: API credentials not configured!
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

echo Starting Dynamic Island...
echo.
echo The app will run in background. You can close this window.
echo To exit: Right-click tray icon (bottom-right) and click Exit
echo.

REM Run in background
start "" venv\Scripts\pythonw.exe dynamic_island.py

echo App started!
