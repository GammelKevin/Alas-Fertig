from flask import Flask
from models import User, MenuItem, MenuCategory, OpeningHours, GalleryCategory, GalleryImage, PageVisit, GalleryView, DailyStats
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisiere die Datenbank
db.init_app(app)

def create_database():
    """Erstellt die Datenbank mit allen Tabellen"""
    with app.app_context():
        print("Erstelle Datenbank-Tabellen...")
        db.create_all()
        print("Datenbank-Tabellen wurden erfolgreich erstellt!")

if __name__ == '__main__':
    create_database()
