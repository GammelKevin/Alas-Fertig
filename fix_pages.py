from models import db, PageVisit
from flask import Flask
from datetime import datetime
import logging
from utils import get_friendly_page_name

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask-App initialisieren
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
db.init_app(app)

with app.app_context():
    # Alle Einträge holen
    all_visits = PageVisit.query.all()
    updated_count = 0
    
    for visit in all_visits:
        # Den aktuellen freundlichen Namen abrufen
        current_friendly_name = visit.page_friendly_name
        
        # Den korrekten freundlichen Namen mit der aktualisierten Funktion berechnen
        correct_friendly_name = get_friendly_page_name(visit.page)
        
        # Wenn der Name unterschiedlich ist oder None war, aktualisieren
        if current_friendly_name != correct_friendly_name:
            logging.info(f"Aktualisiere Besuch ID {visit.id}: page={visit.page}")
            logging.info(f"    Alter Name: {current_friendly_name} -> Neuer Name: {correct_friendly_name}")
            visit.page_friendly_name = correct_friendly_name
            updated_count += 1
    
    # Änderungen speichern
    if updated_count > 0:
        db.session.commit()
        logging.info(f"{updated_count} Einträge aktualisiert")
    else:
        logging.info("Keine Einträge mussten aktualisiert werden")

print("Aktualisierung abgeschlossen.") 