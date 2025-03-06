from flask import Flask
from models import db, PageVisit
from datetime import datetime, timedelta
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Überprüfen wir zuerst die Gesamtzahl der Einträge
    total_entries = PageVisit.query.count()
    logger.info(f"Gesamtzahl der Einträge in PageVisit: {total_entries}")

    # Berechnen wir, wie viele Aufrufe pro Seite existieren
    page_counts = db.session.query(PageVisit.page_friendly_name, db.func.count(PageVisit.id)).\
                 group_by(PageVisit.page_friendly_name).all()
    
    logger.info("Anzahl der Aufrufe pro Seite:")
    for page_name, count in page_counts:
        logger.info(f"  {page_name}: {count}")
    
    # Überprüfen wir die letzten 10 Einträge, um zu sehen, ob es kürzlich doppelte gab
    recent_entries = PageVisit.query.order_by(PageVisit.timestamp.desc()).limit(10).all()
    
    logger.info("\nLetzte 10 Einträge:")
    for entry in recent_entries:
        logger.info(f"ID: {entry.id}, Seite: {entry.page}, Friendly: {entry.page_friendly_name}, Zeit: {entry.timestamp}")
    
    # Suche nach potenziellen Duplikaten (gleiche IP, gleiche Seite, kurzer Zeitabstand)
    logger.info("\nPotenzielle Duplikate (gleiche IP, gleiche Seite, innerhalb von 2 Sekunden):")
    
    # Hole alle Einträge
    all_entries = PageVisit.query.order_by(PageVisit.timestamp).all()
    
    # Durchsuche nach Duplikaten
    potential_duplicates = []
    for i in range(len(all_entries) - 1):
        entry1 = all_entries[i]
        for j in range(i + 1, min(i + 10, len(all_entries))):
            entry2 = all_entries[j]
            
            # Vergleiche IP, Seite und Zeitstempel
            if entry1.ip_address == entry2.ip_address and entry1.page == entry2.page:
                time_diff = entry2.timestamp - entry1.timestamp
                if time_diff.total_seconds() < 2:  # Weniger als 2 Sekunden Unterschied
                    potential_duplicates.append((entry1, entry2, time_diff.total_seconds()))
    
    for entry1, entry2, time_diff in potential_duplicates:
        logger.info(f"Duplikat gefunden: ID1={entry1.id}, ID2={entry2.id}, Seite={entry1.page}, IP={entry1.ip_address}, Zeitdifferenz={time_diff:.2f}s")
    
    logger.info(f"\nGefundene potenzielle Duplikate: {len(potential_duplicates)}")
    
    # Speziell nach den Speisekarte-Einträgen schauen
    menu_entries = PageVisit.query.filter_by(page_friendly_name="Speisekarte").order_by(PageVisit.timestamp).all()
    logger.info(f"\nDetails zu allen Speisekarte-Einträgen ({len(menu_entries)}):")
    for entry in menu_entries:
        logger.info(f"ID: {entry.id}, IP: {entry.ip_address}, Zeit: {entry.timestamp}, Referer: {entry.referer}")

    # Überprüfen wir auch, ob ein @before_request doppelt ausgeführt wird
    logger.info("\nHinweis: Überprüfe die app.py Datei, ob @app.before_request die track_page_visit-Funktion mehrfach aufruft")
    logger.info("Überprüfe auch die JavaScript-Funktionalität in base.html, die möglicherweise mehrere Tracking-Anfragen sendet")

print("Diagnose abgeschlossen. Überprüfe die Logausgabe für Details.") 