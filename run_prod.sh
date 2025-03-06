#!/bin/bash

# Produktions-Startskript

# Umgebungsvariablen setzen
export FLASK_ENV=production
export FLASK_APP=app.py

# Stellen Sie sicher, dass Gunicorn installiert ist
if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn ist nicht installiert. Installation..."
    pip install gunicorn
fi

# Gunicorn-Server mit Konfiguration starten
gunicorn -c gunicorn_config.py wsgi:application
