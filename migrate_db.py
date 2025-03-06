import sqlite3
import os
from app import app, db
from models import MenuCategory

def migrate_database():
    """Migriert die Datenbank, um die neuen Spalten für Analyse-Daten hinzuzufügen"""
    
    # Da der Pfad in der App-Konfiguration 'sqlite:///restaurant.db?charset=utf8mb4' ist,
    # müssen wir nur den Dateinamen extrahieren, nicht den vollständigen Pfad.
    db_path = "restaurant.db"
    
    print(f"Migriere Datenbank: {db_path}")
    
    # Stellen Sie sicher, dass die Datenbank existiert
    if not os.path.exists(db_path):
        print(f"Datenbank nicht gefunden: {db_path}")
        return False
    
    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Füge neue Spalten zur page_visit-Tabelle hinzu...")
        
        # Überprüfen, ob die Spalten bereits existieren
        cursor.execute("PRAGMA table_info(page_visit)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Spalten zur page_visit-Tabelle hinzufügen
        if 'duration' not in columns:
            cursor.execute("ALTER TABLE page_visit ADD COLUMN duration INTEGER")
        if 'browser' not in columns:
            cursor.execute("ALTER TABLE page_visit ADD COLUMN browser VARCHAR(100)")
        if 'operating_system' not in columns:
            cursor.execute("ALTER TABLE page_visit ADD COLUMN operating_system VARCHAR(100)")
        if 'screen_width' not in columns:
            cursor.execute("ALTER TABLE page_visit ADD COLUMN screen_width INTEGER")
        if 'screen_height' not in columns:
            cursor.execute("ALTER TABLE page_visit ADD COLUMN screen_height INTEGER")
        if 'analytics_consent' not in columns:
            cursor.execute("ALTER TABLE page_visit ADD COLUMN analytics_consent BOOLEAN DEFAULT 0")
        
        print("Füge neue Spalten zur daily_stats-Tabelle hinzu...")
        
        # Überprüfen, ob die Spalten bereits existieren
        cursor.execute("PRAGMA table_info(daily_stats)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Spalten zur daily_stats-Tabelle hinzufügen
        if 'avg_duration' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN avg_duration FLOAT DEFAULT 0")
        if 'chrome_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN chrome_users INTEGER DEFAULT 0")
        if 'firefox_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN firefox_users INTEGER DEFAULT 0")
        if 'safari_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN safari_users INTEGER DEFAULT 0")
        if 'edge_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN edge_users INTEGER DEFAULT 0")
        if 'other_browsers' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN other_browsers INTEGER DEFAULT 0")
        if 'windows_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN windows_users INTEGER DEFAULT 0")
        if 'mac_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN mac_users INTEGER DEFAULT 0")
        if 'linux_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN linux_users INTEGER DEFAULT 0")
        if 'ios_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN ios_users INTEGER DEFAULT 0")
        if 'android_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN android_users INTEGER DEFAULT 0")
        if 'other_os' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN other_os INTEGER DEFAULT 0")
        if 'mobile_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN mobile_users INTEGER DEFAULT 0")
        if 'desktop_users' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN desktop_users INTEGER DEFAULT 0")
        if 'consent_count' not in columns:
            cursor.execute("ALTER TABLE daily_stats ADD COLUMN consent_count INTEGER DEFAULT 0")
        
        # Änderungen speichern
        conn.commit()
        print("Migration erfolgreich abgeschlossen!")
        
        return True
    except Exception as e:
        print(f"Fehler bei der Migration: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def add_is_drink_category_column():
    """Fügt die 'is_drink_category'-Spalte zur MenuCategory-Tabelle hinzu, wenn sie noch nicht existiert."""
    conn = None
    try:
        # Finde den Pfad zur Datenbank
        db_path = 'instance/restaurant.db'
        if not os.path.exists(db_path):
            print(f"Datenbank nicht gefunden unter: {db_path}")
            return False
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Prüfen, ob die Spalte bereits existiert
        cursor.execute("PRAGMA table_info(menu_category)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        if 'is_drink_category' not in column_names:
            print("Füge 'is_drink_category'-Spalte hinzu...")
            cursor.execute("ALTER TABLE menu_category ADD COLUMN is_drink_category BOOLEAN DEFAULT 0")
            conn.commit()
            print("Spalte erfolgreich hinzugefügt!")
        else:
            print("Die Spalte 'is_drink_category' existiert bereits.")
        
        conn.close()
        return True
    except Exception as e:
        print(f"Fehler bei der Migration: {str(e)}")
        if conn:
            conn.close()
        return False

if __name__ == "__main__":
    migrate_database()
    with app.app_context():
        success = add_is_drink_category_column()
        if success:
            print("Migration erfolgreich abgeschlossen.")
        else:
            print("Migration fehlgeschlagen.") 