@echo off
REM Produktions-Startskript für Windows

REM Umgebungsvariablen setzen
set FLASK_ENV=production
set FLASK_APP=app.py

REM Überprüfen, ob Waitress installiert ist (Alternative zu Gunicorn für Windows)
pip show waitress > nul 2>&1
if %errorlevel% neq 0 (
    echo Waitress ist nicht installiert. Installation...
    pip install waitress
)

REM Waitress-Server starten
python -m waitress --listen=127.0.0.1:5002 wsgi:application
