from models import db, PageVisit, User
from flask import Flask
from datetime import datetime
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask-App initialisieren
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
db.init_app(app)

with app.app_context():
    # None-Einträge entfernen
    none_entries = PageVisit.query.filter_by(page=None).all()
    if none_entries:
        logging.info(f"Entferne {len(none_entries)} Einträge mit page=None")
        PageVisit.query.filter_by(page=None).delete()
        db.session.commit()
        logging.info("None-Einträge wurden gelöscht")
    else:
        logging.info("Keine None-Einträge gefunden")
    
    # Überprüfen der aktuellen Aufrufe für die Startseite
    startseite_visits = PageVisit.query.filter_by(page="/").all()
    logging.info(f"Anzahl der Startseiten-Besuche in der Datenbank: {len(startseite_visits)}")
    
    for visit in startseite_visits:
        logging.info(f"Besuch ID: {visit.id}, Zeitpunkt: {visit.timestamp}")
    
    # Überprüfen aller erfassten Seiten
    all_pages = db.session.query(PageVisit.page, db.func.count(PageVisit.id)).group_by(PageVisit.page).all()
    logging.info("Aktuelle Seitenstatistik:")
    for page, count in all_pages:
        logging.info(f"Seite: {page}, Aufrufe: {count}")

print("Skript erfolgreich ausgeführt.") 