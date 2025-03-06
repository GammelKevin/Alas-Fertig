#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, db
from models import DailyStats
from datetime import datetime, timedelta

def list_stats():
    """Listet alle vorhandenen Statistikdaten auf"""
    with app.app_context():
        # Alle Statistikdaten abrufen
        stats = DailyStats.query.order_by(DailyStats.date.desc()).all()
        
        if not stats:
            print("Keine Statistikdaten gefunden.")
            return
        
        print(f"Gefundene Statistikdaten: {len(stats)}")
        print("\nDie neuesten 10 Einträge:")
        
        for i, stat in enumerate(stats[:10]):
            print(f"{i+1}. Datum: {stat.date}, Besuche: {stat.total_visits}, "
                  f"Eindeutige Besucher: {stat.unique_visitors}, "
                  f"Galerieaufrufe: {stat.gallery_views}")

if __name__ == "__main__":
    list_stats() 