@echo off
:: Spotify Watcher - Starts silently in background
:: Add this to Windows Startup folder for auto-start with Windows

cd /d "%~dp0"

:: Check if venv exists and use it
if exist "venv\Scripts\pythonw.exe" (
    start "" "venv\Scripts\pythonw.exe" spotify_watcher.py
) else if exist "dynamic_island_env\Scripts\pythonw.exe" (
    start "" "dynamic_island_env\Scripts\pythonw.exe" spotify_watcher.py
) else (
    start "" pythonw spotify_watcher.py
)
