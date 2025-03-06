from flask import Flask
import os
import sys

print("Script zur Diagnose der doppelten Zählung von Seitenaufrufen gestartet")
print(f"Aktuelles Verzeichnis: {os.getcwd()}")
print(f"Existiert instance/restaurant.db: {os.path.exists('instance/restaurant.db')}")

try:
    print("\nVersuche, die Datenbankverbindung zu testen...")
    from models import db, PageVisit
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/restaurant.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        try:
            count = PageVisit.query.count()
            print(f"Verbindung zur Datenbank erfolgreich, {count} Einträge gefunden")
            
            print("\nPrüfe app.py auf mögliche Probleme...")
            with open('app.py', 'r', encoding='utf-8') as f:
                app_code = f.read()
                
            # Zähle, wie oft track_page_visit aufgerufen wird
            track_calls = app_code.count('track_page_visit(')
            print(f"Anzahl der Aufrufe von track_page_visit in app.py: {track_calls}")
            
            # Prüfe auf doppelte before_request-Dekoratoren
            before_requests = app_code.count('@app.before_request')
            print(f"Anzahl der @app.before_request in app.py: {before_requests}")
            
            print("\nPrüfe utils.py auf mögliche Probleme...")
            with open('utils.py', 'r', encoding='utf-8') as f:
                utils_code = f.read()
            
            # Suche nach der track_page_visit-Funktion
            if 'def track_page_visit(' in utils_code:
                print("track_page_visit-Funktion in utils.py gefunden")
                
                # Extrahiere die Funktion zur Analyse
                start_idx = utils_code.find('def track_page_visit(')
                end_idx = utils_code.find('def ', start_idx + 1)
                if end_idx == -1:
                    end_idx = len(utils_code)
                    
                track_function = utils_code[start_idx:end_idx]
                print(f"\nAuszug aus der track_page_visit-Funktion:")
                print(track_function[:500] + "..." if len(track_function) > 500 else track_function)
                
                # Prüfe, ob die Funktion mehrfach Einträge erstellt
                creates_entry = 'db.session.add(' in track_function
                print(f"Erstellt die Funktion Datenbankeinträge: {creates_entry}")
                
            print("\nPrüfe JavaScript-Code in base.html...")
            try:
                with open('templates/base.html', 'r', encoding='utf-8') as f:
                    base_html = f.read()
                    
                if 'fetch(\'/get_visit_id' in base_html:
                    print("get_visit_id wird über fetch in base.html aufgerufen")
                    
                    # Prüfe auf mehrfache Aufrufe
                    calls = base_html.count('fetch(\'/get_visit_id')
                    print(f"Anzahl der fetch-Aufrufe für get_visit_id: {calls}")
                    
                    # Finde den JavaScript-Code, der die Aufrufe macht
                    fetch_idx = base_html.find('fetch(\'/get_visit_id')
                    start_of_script = base_html.rfind('<script', 0, fetch_idx)
                    end_of_script = base_html.find('</script>', fetch_idx)
                    
                    if start_of_script != -1 and end_of_script != -1:
                        js_code = base_html[start_of_script:end_of_script]
                        print(f"\nRelevanter JavaScript-Code:")
                        print(js_code[:500] + "..." if len(js_code) > 500 else js_code)
            except Exception as e:
                print(f"Fehler beim Lesen von base.html: {e}")
                
            print("\nFazit: Überprüfe, ob:")
            print("1. Die before_request-Funktion mehrfach aufgerufen wird")
            print("2. Der JavaScript-Code mehrfach Tracking-Anfragen sendet")
            print("3. Die track_page_visit-Funktion in utils.py unter bestimmten Bedingungen mehrfach Einträge erstellt")
                
        except Exception as e:
            print(f"Fehler bei der Abfrage der Datenbank: {e}")
    
except Exception as e:
    print(f"Allgemeiner Fehler: {e}")
    print("Stack trace:")
    import traceback
    traceback.print_exc()

print("\nDiagnose abgeschlossen.") 