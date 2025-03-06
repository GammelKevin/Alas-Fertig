from app import app, db
import sqlite3
import os

def verify_table():
    with app.app_context():
        try:
            # Pfad zur Datenbank ermitteln
            db_path = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if db_path.startswith('sqlite:///'):
                db_path = db_path[10:]  # 'sqlite:///' entfernen
                
            # Frage-Zeichen und alles danach entfernen (Parameter wie charset=utf8mb4)
            if '?' in db_path:
                db_path = db_path.split('?')[0]
                
            print(f"Datenbankpfad: {db_path}")
            if not os.path.exists(db_path):
                print(f"Datenbank existiert nicht unter {db_path}")
                return False
                
            # Datenbankgröße überprüfen
            file_size = os.path.getsize(db_path)
            print(f"Datenbankgröße: {file_size} Bytes")
                
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Alle Tabellen auflisten
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print("Vorhandene Tabellen:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Überprüfen, ob die Tabelle existiert
            if ('menu_category',) in tables:
                # Spalten der Tabelle auflisten
                cursor.execute("PRAGMA table_info(menu_category)")
                columns = cursor.fetchall()
                print("\nSpalten in menu_category:")
                for column in columns:
                    print(f"  - {column[1]} ({column[2]})")
                    
                # Überprüfen, ob is_drink_category existiert
                column_names = [column[1] for column in columns]
                if 'is_drink_category' in column_names:
                    print("\nis_drink_category existiert in der Tabelle!")
                else:
                    print("\nis_drink_category fehlt in der Tabelle!")
            else:
                print("\nTabelle menu_category existiert nicht!")
                
            conn.close()
            return True
        except Exception as e:
            print(f"Fehler bei der Überprüfung: {str(e)}")
            return False

if __name__ == "__main__":
    verify_table() 