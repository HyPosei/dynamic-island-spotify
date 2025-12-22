@echo off
chcp 65001 >nul
echo ══════════════════════════════════════════════════
echo   Dynamic Island Spotify - Kaldırma / Uninstall
echo ══════════════════════════════════════════════════
echo.

echo [1/3] Uygulama kapatılıyor / Closing application...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
taskkill /F /IM dynamic_island.exe 2>nul
timeout /t 2 >nul

echo [2/3] Başlangıç kaydı siliniyor / Removing startup entry...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DynamicIslandSpotify" /f 2>nul

echo [3/3] Ayarlar siliniyor / Removing settings...
reg delete "HKCU\Software\DynamicIsland" /f 2>nul

echo.
echo ══════════════════════════════════════════════════
echo   ✓ Uygulama kapatıldı ve kayıtlar silindi!
echo   ✓ Application closed and registry cleaned!
echo.
echo   Şimdi bu klasörü silebilirsiniz.
echo   You can now delete this folder.
echo ══════════════════════════════════════════════════
echo.
pause
