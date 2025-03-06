from app import app, db
import sqlite3
from utils import get_friendly_page_name

def update_schema():
    """Aktualisiert das Datenbankschema und fügt die neue Spalte page_friendly_name zur PageVisit-Tabelle hinzu"""
    try:
        with app.app_context():
            # Verbindung zur SQLite-Datenbank herstellen
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            
            # Prüfen, ob die Spalte bereits existiert
            cursor.execute("PRAGMA table_info(page_visit)")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            
            # Spalte hinzufügen, wenn sie nicht existiert
            if 'page_friendly_name' not in column_names:
                print("Füge Spalte 'page_friendly_name' zur Tabelle PageVisit hinzu...")
                cursor.execute("ALTER TABLE page_visit ADD COLUMN page_friendly_name TEXT")
                
                # Aktualisiere bestehende Einträge mit freundlichen Namen
                print("Aktualisiere bestehende Einträge...")
                cursor.execute("SELECT id, page FROM page_visit")
                entries = cursor.fetchall()
                for entry_id, page in entries:
                    friendly_name = get_friendly_page_name(page)
                    cursor.execute("UPDATE page_visit SET page_friendly_name = ? WHERE id = ?", (friendly_name, entry_id))
                
                conn.commit()
                print("Schema-Update abgeschlossen.")
            else:
                print("Spalte 'page_friendly_name' existiert bereits.")
            
            conn.close()
    except Exception as e:
        print(f"Fehler beim Aktualisieren des Schemas: {e}")

if __name__ == "__main__":
    update_schema() 