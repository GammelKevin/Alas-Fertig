from models import db, PageVisit, DailyStats, User
from flask import Flask
from datetime import datetime, timedelta
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask-App initialisieren
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
db.init_app(app)

def fix_statistics():
    with app.app_context():
        # 1. None-Einträge entfernen
        none_entries = PageVisit.query.filter_by(page=None).all()
        if none_entries:
            logging.info(f"Entferne {len(none_entries)} Einträge mit page=None")
            PageVisit.query.filter_by(page=None).delete()
            db.session.commit()
            logging.info("None-Einträge wurden gelöscht")
        else:
            logging.info("Keine None-Einträge gefunden")
        
        # 2. Neuberechnung der Tagesstatistiken für den heutigen Tag
        today = datetime.now().date()
        today_stats = DailyStats.query.filter_by(date=today).first()
        
        if today_stats:
            logging.info("Lösche vorhandene Tagesstatistik für heute")
            db.session.delete(today_stats)
            db.session.commit()
        
        # Erstelle neue Tagesstatistik
        logging.info("Erstelle neue Tagesstatistik für heute")
        today_stats = DailyStats(
            date=today,
            total_visits=0,
            unique_visitors=0,
            gallery_views=0,
            consent_count=0,
            chrome_users=0,
            firefox_users=0,
            safari_users=0,
            edge_users=0,
            other_browsers=0,
            windows_users=0,
            mac_users=0,
            linux_users=0,
            ios_users=0,
            android_users=0,
            other_os=0,
            mobile_users=0,
            desktop_users=0
        )
        db.session.add(today_stats)
        db.session.commit()
        
        # 3. Berechnung der Statistiken auf Basis der vorhandenen Besuche für heute
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        # Alle Besuche für heute
        today_visits = PageVisit.query.filter(
            PageVisit.timestamp >= today_start,
            PageVisit.timestamp <= today_end
        ).all()
        
        # Zähle die Gesamtbesuche
        today_stats.total_visits = len(today_visits)
        
        # Zähle eindeutige Besucher (basierend auf IP-Adresse)
        unique_ips = set()
        for visit in today_visits:
            if hasattr(visit, 'ip_address'):
                unique_ips.add(visit.ip_address)
        today_stats.unique_visitors = len(unique_ips)
        
        # Aktualisiere Browser-Statistiken
        for visit in today_visits:
            if visit.browser == 'Chrome':
                today_stats.chrome_users += 1
            elif visit.browser == 'Firefox':
                today_stats.firefox_users += 1
            elif visit.browser == 'Safari':
                today_stats.safari_users += 1
            elif visit.browser == 'Edge':
                today_stats.edge_users += 1
            else:
                today_stats.other_browsers += 1
            
            # Betriebssystem-Statistiken aktualisieren
            if visit.operating_system == 'Windows':
                today_stats.windows_users += 1
            elif visit.operating_system == 'Mac OS':
                today_stats.mac_users += 1
            elif visit.operating_system == 'Linux':
                today_stats.linux_users += 1
            elif visit.operating_system == 'iOS':
                today_stats.ios_users += 1
            elif visit.operating_system == 'Android':
                today_stats.android_users += 1
            else:
                today_stats.other_os += 1
            
            # Mobile/Desktop-Statistiken
            if hasattr(visit, 'is_mobile') and visit.is_mobile:
                today_stats.mobile_users += 1
            else:
                today_stats.desktop_users += 1
            
            # Cookie-Zustimmung
            if hasattr(visit, 'analytics_consent') and visit.analytics_consent:
                today_stats.consent_count += 1
        
        db.session.commit()
        
        # Debug-Info
        logging.info(f"Aktualisierte Statistiken für heute ({today}):")
        logging.info(f"Gesamtbesuche: {today_stats.total_visits}")
        logging.info(f"Eindeutige Besucher: {today_stats.unique_visitors}")
        
        # Überprüfen der aktuellen Seitenbesuche
        page_visits = db.session.query(
            PageVisit.page, 
            db.func.count(PageVisit.id).label('count')
        ).group_by(
            PageVisit.page
        ).order_by(
            db.func.count(PageVisit.id).desc()
        ).all()
        
        logging.info("Aktuelle Seitenstatistik:")
        for page, count in page_visits:
            logging.info(f"Seite: {page}, Aufrufe: {count}")
        
        return True

if __name__ == "__main__":
    if fix_statistics():
        print("Statistiken wurden erfolgreich repariert!")
    else:
        print("Fehler beim Reparieren der Statistiken.") 