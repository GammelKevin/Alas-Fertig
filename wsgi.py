#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
WSGI-Einstiegspunkt für Produktionsserver wie Gunicorn oder uWSGI.
'''

import os
import sys

# Setze die Umgebungsvariablen für die Produktion
os.environ['FLASK_ENV'] = 'production'

# Füge das aktuelle Verzeichnis zum Pfad hinzu
sys.path.insert(0, os.path.dirname(__file__))

# Importiere die Flask-App
from app import app as application

if __name__ == "__main__":
    # Bei direktem Aufruf die App starten
    application.run()
