from models import db, PageVisit, DailyStats
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
    # None-Einträge suchen
    none_entries = PageVisit.query.filter_by(page="None").all()
    if none_entries:
        logging.info(f"Gefunden: {len(none_entries)} Einträge mit page='None' (als String)")
        # Details anzeigen
        for visit in none_entries:
            logging.info(f"Besuch ID: {visit.id}, Zeitstempel: {visit.timestamp}, page: '{visit.page}'")
    else:
        logging.info("Keine Einträge mit page='None' (als String) gefunden")

    # Nun suchen wir nach NULL-Werten (None als Python-Objekt)
    null_entries = PageVisit.query.filter(PageVisit.page.is_(None)).all()
    if null_entries:
        logging.info(f"Gefunden: {len(null_entries)} Einträge mit page=NULL (None als Objekt)")
        # Details anzeigen
        for visit in null_entries:
            logging.info(f"Besuch ID: {visit.id}, Zeitstempel: {visit.timestamp}, page: {visit.page}")
    else:
        logging.info("Keine Einträge mit page=NULL (None als Objekt) gefunden")
    
    # Alle page-Werte in der Datenbank auflisten
    page_values = db.session.query(PageVisit.page, db.func.count(PageVisit.id)).group_by(PageVisit.page).all()
    logging.info("Alle verschiedenen page-Werte in der Datenbank:")
    for page, count in page_values:
        logging.info(f"page: '{page}', Anzahl: {count}")
    
    # Prüfen, ob es Einträge mit dem Wort "None" als String gibt
    word_none_entries = PageVisit.query.filter(PageVisit.page == "None").all()
    if word_none_entries:
        logging.info(f"Es gibt {len(word_none_entries)} Einträge mit page='None' als String!")
    else:
        logging.info("Keine Einträge mit dem String 'None' als page gefunden")

print("Analyse abgeschlossen.") 