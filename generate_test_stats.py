#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, db
from models import DailyStats, PageVisit, GalleryView, GalleryImage, GalleryCategory
from datetime import datetime, timedelta
import random

def generate_test_stats():
    """Generiert Testdaten für die Statistikseite"""
    with app.app_context():
        # Lösche vorhandene Statistiken (optional)
        # DailyStats.query.delete()
        # PageVisit.query.delete()
        
        # Erzeuge Statistiken für die letzten 30 Tage
        today = datetime.now().date()
        
        # Erstelle eine Galerie-Kategorie, falls keine vorhanden ist
        gallery_category = GalleryCategory.query.first()
        if not gallery_category:
            gallery_category = GalleryCategory(name="Testkategorie")
            db.session.add(gallery_category)
            db.session.commit()
        
        # Erstelle einige Galerie-Bilder, falls keine vorhanden sind
        gallery_images = GalleryImage.query.all()
        if not gallery_images:
            for i in range(1, 6):
                image = GalleryImage(
                    title=f"Testbild {i}", 
                    image_path=f"test{i}.jpg",
                    category_id=gallery_category.id
                )
                db.session.add(image)
            db.session.commit()
            gallery_images = GalleryImage.query.all()
        
        # Erstelle Statistiken für die letzten 30 Tage
        for i in range(30):
            date = today - timedelta(days=i)
            
            # Prüfe, ob bereits Daten für diesen Tag existieren
            existing_stats = DailyStats.query.filter_by(date=date).first()
            if existing_stats:
                print(f"Statistiken für {date} existieren bereits, überspringe...")
                continue
            
            # Zufallswerte für die Statistiken
            visits = random.randint(50, 200)
            unique_visitors = random.randint(30, visits)
            gallery_views = random.randint(10, 80)
            
            # Browser-Verteilung
            chrome = random.randint(20, 60)
            firefox = random.randint(10, 30)
            safari = random.randint(5, 20)
            edge = random.randint(5, 15)
            other_browsers = random.randint(0, 10)
            
            # Betriebssystem-Verteilung
            windows = random.randint(20, 50)
            mac = random.randint(10, 30)
            linux = random.randint(5, 15)
            ios = random.randint(10, 25)
            android = random.randint(10, 25)
            other_os = random.randint(0, 5)
            
            # Gerätetyp-Verteilung
            mobile = random.randint(20, 60)
            desktop = random.randint(20, 60)
            
            # Cookie-Zustimmung
            consent_count = random.randint(int(visits * 0.6), visits)
            
            # Durchschnittliche Verweildauer (2-10 Minuten)
            avg_duration = random.randint(120, 600)
            
            # Erstelle DailyStats-Eintrag
            stats = DailyStats(
                date=date,
                total_visits=visits,
                unique_visitors=unique_visitors,
                gallery_views=gallery_views,
                avg_duration=avg_duration,
                chrome_users=chrome,
                firefox_users=firefox,
                safari_users=safari,
                edge_users=edge,
                other_browsers=other_browsers,
                windows_users=windows,
                mac_users=mac,
                linux_users=linux,
                ios_users=ios,
                android_users=android,
                other_os=other_os,
                mobile_users=mobile,
                desktop_users=desktop,
                consent_count=consent_count
            )
            db.session.add(stats)
            
            # Erstelle einige PageVisit-Einträge für diesen Tag
            pages = ['/', '/speisekarte', '/galerie', '/kontakt', '/oeffnungszeiten']
            for _ in range(visits):
                page = random.choice(pages)
                timestamp = datetime.combine(date, datetime.min.time()) + timedelta(
                    hours=random.randint(10, 22),
                    minutes=random.randint(0, 59)
                )
                
                visit = PageVisit(
                    page=page,
                    page_friendly_name=page.replace('/', '').capitalize() if page != '/' else 'Homepage',
                    ip_address=f"192.168.1.{random.randint(1, 254)}",
                    user_agent="Mozilla/5.0",
                    timestamp=timestamp,
                    analytics_consent=random.choice([True, True, True, False]),  # 75% Zustimmungsrate
                    browser=random.choice(["Chrome", "Firefox", "Safari", "Edge", "Other"]),
                    operating_system=random.choice(["Windows", "Mac", "Linux", "iOS", "Android", "Other"]),
                    duration=random.randint(30, 1200)  # 30 Sekunden bis 20 Minuten
                )
                db.session.add(visit)
            
            # Erstelle einige GalleryView-Einträge für diesen Tag
            for _ in range(gallery_views):
                image = random.choice(gallery_images)
                timestamp = datetime.combine(date, datetime.min.time()) + timedelta(
                    hours=random.randint(10, 22),
                    minutes=random.randint(0, 59)
                )
                
                view = GalleryView(
                    image_id=image.id,
                    timestamp=timestamp,
                    ip_address=f"192.168.1.{random.randint(1, 254)}"
                )
                db.session.add(view)
        
        # Speichere alle Änderungen
        db.session.commit()
        print(f"Testdaten für die letzten 30 Tage wurden generiert.")

if __name__ == "__main__":
    generate_test_stats() 