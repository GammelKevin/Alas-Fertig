#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Führe zuerst die Migration aus
python migrations.py

# Dann initialisiere die restliche DB
python init_db.py
