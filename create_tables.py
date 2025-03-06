from app import app, db
from models import User, MenuItem, MenuCategory, OpeningHours, GalleryImage, PageVisit, GalleryView, DailyStats, GalleryCategory

def create_tables():
    with app.app_context():
        try:
            # Tabellen erstellen
            db.create_all()
            print("Datenbanktabellen wurden erstellt")
            return True
        except Exception as e:
            print(f"Fehler beim Erstellen der Tabellen: {str(e)}")
            return False

if __name__ == "__main__":
    success = create_tables()
    print(f"Skript abgeschlossen. Erfolgreich: {success}") 