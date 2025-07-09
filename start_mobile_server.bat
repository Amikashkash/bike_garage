@echo off
echo 📱 מתחיל שרת Django לגישה ממובייל...
echo.

REM קבלת כתובת IP של המחשב
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /R /C:"IPv4.*192\.168\." /C:"IPv4.*10\." /C:"IPv4.*172\."') do (
    for /f "tokens=1" %%j in ("%%i") do set LOCAL_IP=%%j
)

if defined LOCAL_IP (
    echo 🌐 כתובת IP מקומית: %LOCAL_IP%
    echo 📱 גש מהמובייל לכתובת: http://%LOCAL_IP%:8000
    echo.
    echo 💡 וודא שהמחשב והמובייל חיברים לאותה רשת WiFi
    echo.
    echo ⚠️  לעצירת השרת לחץ Ctrl+C
    echo.
    
    python manage.py runserver 0.0.0.0:8000
) else (
    echo ❌ לא מצאתי כתובת IP מקומית
    echo 💡 בדוק שאתה מחובר לרשת WiFi
    echo.
    echo מתחיל שרת רגיל על localhost...
    python manage.py runserver
)

pause
