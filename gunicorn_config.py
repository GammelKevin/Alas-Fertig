#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Gunicorn-Konfigurationsdatei für die Produktionsumgebung.
'''

import multiprocessing
import os

# Setze die Umgebungsvariablen für die Produktion
os.environ['FLASK_ENV'] = 'production'

# Anzahl der Worker (2-4 x Anzahl der Kerne)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker-Klasse
worker_class = 'sync'

# Binde an localhost
bind = '127.0.0.1:5002'

# Arbeitsverzeichnis
chdir = os.path.dirname(__file__)

# Maximale Anzahl gleichzeitiger Clients
max_requests = 1000

# Zufällige Variation für max_requests
max_requests_jitter = 50

# Timeout-Einstellungen
timeout = 30
keepalive = 2

# Protokollierung
loglevel = 'info'
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'

# Stelle sicher, dass das Log-Verzeichnis existiert
os.makedirs('logs', exist_ok=True)

# Stille Protokollierung für die Gesundheitsprüfung
accesslog_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Sicherheitseinstellungen
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
