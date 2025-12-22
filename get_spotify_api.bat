@echo off
chcp 65001 >nul
title Spotify API Anahtari Al
color 0B

echo.
echo   ================================================================
echo.
echo     SPOTIFY API ANAHTARI ALMA KILAVUZU
echo.
echo   ================================================================
echo.
echo   Bu uygulama Spotify API anahtarlarina ihtiyac duyar.
echo   Anahtarlari almak UCRETSIZ ve sadece 2 dakika surer!
echo.
echo   ----------------------------------------------------------------
echo.
echo   ADIM ADIM TALIMATLAR:
echo.
echo   1. Simdi acilacak sayfada Spotify hesabinizla giris yapin
echo.
echo   2. "Create App" butonuna tiklayin
echo.
echo   3. Formu doldurun:
echo      - App name: Dynamic Island
echo      - App description: Spotify controller
echo      - Redirect URI: http://localhost:8888/callback
echo      - Web API secenegini isaretleyin
echo.
echo   4. "Save" tiklayin
echo.
echo   5. Olusturulan uygulamaya tiklayin
echo.
echo   6. "Settings" butonuna tiklayin
echo.
echo   7. "Client ID" ve "Client Secret" degerlerini kopyalayin
echo.
echo   8. Bu bilgileri "setup.bat" calistirdiginizda gireceksiniz
echo.
echo   ----------------------------------------------------------------
echo.
echo   NOT: Her kullanici kendi API anahtarlarini almalidir!
echo.
echo   ----------------------------------------------------------------
echo.
echo   Spotify Developer sayfasini acmak icin ENTER'a basin...
pause >nul

echo.
echo   Tarayici aciliyor...
explorer "https://developer.spotify.com/dashboard"

echo.
echo   ----------------------------------------------------------------
echo.
echo   Tarayici acildi! Yukardaki talimatlari takip edin.
echo.
echo   Tarayici acilmadi mi? Su adresi manuel olarak acin:
echo   https://developer.spotify.com/dashboard
echo.
echo   Anahtarlari aldiktan sonra "setup.bat" dosyasini calistirin.
echo.
echo   ----------------------------------------------------------------
echo.
pause
