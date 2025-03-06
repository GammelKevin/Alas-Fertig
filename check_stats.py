#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from models import DailyStats, PageVisit
from datetime import datetime

def check_daily_stats():
    """Überprüft die heutige Tagesstatistik"""
    with app.app_context():
        today = datetime.now().date()
        stats = DailyStats.query.filter_by(date=today).first()
        
        if stats:
            print(f"Tagesstatistik für {today}:")
            print(f"Durchschnittliche Verweildauer: {stats.avg_duration:.2f} Sekunden")
            print(f"Gesamtbesuche: {stats.total_visits}")
            print(f"Einzigartige Besucher: {stats.unique_visitors}")
        else:
            print(f"Keine Tagesstatistik für {today} gefunden.")
        
        # Besuche mit Verweildauer prüfen
        visits_with_duration = PageVisit.query.filter(
            PageVisit.timestamp >= datetime.combine(today, datetime.min.time()),
            PageVisit.duration.isnot(None),
            PageVisit.analytics_consent == True
        ).all()
        
        print(f"\nBesuche mit Verweildauer heute: {len(visits_with_duration)}")
        
        if visits_with_duration:
            print("\nDie neuesten 5 Besuche mit Verweildauer:")
            for i, visit in enumerate(sorted(visits_with_duration, key=lambda v: v.timestamp, reverse=True)[:5]):
                print(f"{i+1}. ID: {visit.id}, Seite: {visit.page}, Dauer: {visit.duration}s, Zeit: {visit.timestamp}")
            
            total_duration = sum(v.duration for v in visits_with_duration)
            avg_duration = total_duration / len(visits_with_duration)
            print(f"\nManuelle Berechnung:")
            print(f"Gesamtdauer: {total_duration}s")
            print(f"Durchschnitt: {avg_duration:.2f}s")

if __name__ == "__main__":
    check_daily_stats() 