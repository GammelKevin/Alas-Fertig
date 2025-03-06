#!/bin/bash

# Entwicklungs-Startskript

# Umgebungsvariablen setzen
export FLASK_ENV=development
export FLASK_APP=app.py

# Flask-Server starten
python app.py
