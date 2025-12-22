@echo off
chcp 65001 >nul 2>&1
title Dynamic Island EXE Builder
cd /d "%~dp0"

echo.
echo   ================================================================
echo   Dynamic Island EXE Builder
echo   ================================================================
echo.

:: Check if venv exists
if not exist venv (
    echo   ERROR: Run setup.bat first!
    pause
    exit /b 1
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install PyInstaller if not installed
echo   Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo   Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo   Building EXE file...
echo   (This may take a few minutes)
echo.

:: Build the exe
python -m PyInstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name "DynamicIslandSpotify" ^
    --icon=NONE ^
    --hidden-import=PySide6.QtCore ^
    --hidden-import=PySide6.QtGui ^
    --hidden-import=PySide6.QtWidgets ^
    --hidden-import=spotipy ^
    --hidden-import=spotipy.oauth2 ^
    --hidden-import=dotenv ^
    --hidden-import=PIL ^
    --hidden-import=colorthief ^
    --hidden-import=requests ^
    --hidden-import=psutil ^
    dynamic_island.py

if errorlevel 1 (
    echo.
    echo   ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo   SUCCESS: EXE created!
echo   Location: dist\DynamicIslandSpotify.exe
echo.

:: Copy cache file if exists
if exist .spotify_cache (
    copy .spotify_cache dist\.spotify_cache >nul
    echo   Cache file copied to dist folder.
)

echo.
echo   You can now run dist\DynamicIslandSpotify.exe
echo.
pause
