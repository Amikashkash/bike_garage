@echo off
cd /d C:\bikegarage
echo === Testing Django System ===
echo.

echo 1. Checking migrations...
C:\bikegarage\venv\Scripts\python.exe manage.py showmigrations workshop

echo.
echo 2. Running migrations...
C:\bikegarage\venv\Scripts\python.exe manage.py migrate

echo.
echo 3. Testing stuck functionality...
C:\bikegarage\venv\Scripts\python.exe test_stuck_functionality.py

echo.
echo 4. Checking if server is accessible...
curl -s -o nul -w "HTTP Status: %%{http_code}" http://127.0.0.1:8000/

echo.
echo === Test Complete ===
pause
