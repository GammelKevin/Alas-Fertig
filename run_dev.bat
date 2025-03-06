@echo off
REM Entwicklungs-Startskript für Windows

REM Umgebungsvariablen setzen
set FLASK_ENV=development
set FLASK_APP=app.py

REM Flask-Server starten
python app.py
