@echo off
echo Starting bike garage server with demo data...

REM Create demo data
echo Creating demo data...
python create_demo_data.py

REM Start server
echo Starting Django server...
python manage.py runserver 8080

pause
