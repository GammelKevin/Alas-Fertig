#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, db
from models import PageVisit, DailyStats
from datetime import datetime, timedelta
import random

def add_test_visits():
    """Fügt Testbesuche mit unterschiedlichen Verweildauern hinzu"""
    with app.app_context():
        today = datetime.now().date()
        
        # Stellen Sie sicher, dass die heutige Statistik existiert
        stats = DailyStats.query.filter_by(date=today).first()
        if not stats:
            stats = DailyStats(
                date=today,
                total_visits=0,
                unique_visitors=0,
                gallery_views=0
            )
            db.session.add(stats)
            db.session.commit()
        
        # Löschen Sie alle bestehenden Testbesuche mit der Test-IP (optional)
        PageVisit.query.filter(
            PageVisit.timestamp >= datetime.combine(today, datetime.min.time()),
            PageVisit.timestamp <= datetime.combine(today, datetime.max.time()),
            PageVisit.ip_address == '192.0.2.123'  # Verwenden einer speziellen Test-IP
        ).delete()
        
        # Verschiedene Seiten für die Testbesuche
        pages = ['/', '/speisekarte', '/galerie', '/kontakt', '/impressum']
        
        # Verschiedene Verweildauern (von 10 Sekunden bis 5 Minuten)
        durations = [10, 30, 60, 120, 180, 240, 300]
        
        # Hinzufügen von 10 Testbesuchen
        base_time = datetime.now() - timedelta(hours=1)
        
        for i in range(10):
            page = random.choice(pages)
            duration = random.choice(durations)
            timestamp = base_time + timedelta(minutes=i*5)
            
            visit = PageVisit(
                page=page,
                timestamp=timestamp,
                ip_address='192.0.2.123',  # Spezielle Test-IP
                user_agent='Test Browser',
                duration=duration,
                analytics_consent=True
            )
            
            db.session.add(visit)
        
        db.session.commit()
        
        print(f"10 Testbesuche mit unterschiedlichen Verweildauern hinzugefügt.")
        print("Besuche:")
        for visit in PageVisit.query.filter_by(ip_address='192.0.2.123').all():
            print(f"ID: {visit.id}, Seite: {visit.page}, Dauer: {visit.duration}s, Zeit: {visit.timestamp}")
        
        # Stellen Sie sicher, dass die Tagesstatistik aktualisiert wird
        from utils import update_visit_duration
        for visit in PageVisit.query.filter_by(ip_address='192.0.2.123').all():
            update_visit_duration(visit.id, visit.duration)

if __name__ == "__main__":
    add_test_visits() 