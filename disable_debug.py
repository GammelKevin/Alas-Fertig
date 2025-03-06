#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Dieses Skript deaktiviert den Debug-Modus und konfiguriert die Anwendung für eine sicherere Produktionsumgebung.
Es erstellt auch eine separate Entwicklungskonfiguration für lokale Tests.
'''

import os
import re
import datetime
import random
import string
import configparser

def log_message(message):
    """Protokolliert eine Nachricht mit Zeitstempel"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    # Auch in eine Datei schreiben
    with open('security_fixes.log', 'a', encoding='utf-8') as log_file:
        log_file.write(log_message + "\n")

def generate_secret_key(length=32):
    """Generiert einen zufälligen Secret Key für Flask"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def create_config_files():
    """Erstellt Konfigurations-Dateien für Entwicklung und Produktion"""
    
    # Stelle sicher, dass das Instance-Verzeichnis existiert
    os.makedirs('instance', exist_ok=True)
    
    # Konfigurationsdatei für die Produktion
    production_config = """# Produktionskonfiguration
SECRET_KEY = '{}'
DEBUG = False
TESTING = False
DATABASE = 'instance/restaurant.db'
UPLOAD_FOLDER = 'static/uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB Limit für Datei-Uploads
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = 1800  # 30 Minuten
""".format(generate_secret_key())
    
    with open('instance/production.cfg', 'w') as f:
        f.write(production_config)
    
    # Konfigurationsdatei für die Entwicklung
    dev_config = """# Entwicklungskonfiguration
SECRET_KEY = 'dev-key-not-secure-for-production'
DEBUG = True
TESTING = False
DATABASE = 'instance/restaurant.db'
UPLOAD_FOLDER = 'static/uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB Limit für Datei-Uploads
SESSION_COOKIE_SECURE = False  # Für lokale Entwicklung ohne HTTPS
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = 3600  # 60 Minuten
"""
    
    with open('instance/development.cfg', 'w') as f:
        f.write(dev_config)
    
    log_message("Konfigurationsdateien wurden erstellt: instance/production.cfg und instance/development.cfg")
    return True

def modify_app_py_for_config():
    """Modifiziert app.py um Konfigurationsdateien zu verwenden"""
    app_py_path = 'app.py'
    
    if not os.path.exists(app_py_path):
        log_message(f"Fehler: {app_py_path} nicht gefunden")
        return False
    
    try:
        # Datei lesen
        with open(app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Überprüfen, ob die Konfiguration bereits aktualisiert wurde
        if "app.config.from_pyfile" in content:
            log_message("Konfiguration scheint bereits in app.py aktualisiert zu sein.")
            return True
        
        # Suchen nach der app-Initialisierung
        app_init_pattern = r'app = Flask\(__name__\)'
        
        if not re.search(app_init_pattern, content):
            log_message("Konnte die Flask-App-Initialisierung nicht finden.")
            return False
        
        # Suchen nach der app.config-Einstellung
        config_section = re.search(r'app = Flask\(__name__\)(.*?)(?=@app\.|\n\n)', content, re.DOTALL)
        
        if not config_section:
            log_message("Konnte den Konfigurationsabschnitt nicht finden.")
            return False
        
        # Extrahieren des Konfigurationsabschnitts
        config_text = config_section.group(1)
        
        # Ersetzen der alten Konfiguration durch die neue
        new_config = """
# Konfiguration basierend auf Umgebung laden
if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_pyfile('instance/production.cfg')
else:
    app.config.from_pyfile('instance/development.cfg')

# Stellen Sie sicher, dass der DEBUG-Modus in der Produktion deaktiviert ist
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
"""
        
        # Ersetzen des Konfigurationsabschnitts
        new_content = content.replace(config_text, new_config)
        
        # Ersetzen von expliziten DEBUG=True-Anweisungen
        new_content = re.sub(r"app\.config\['DEBUG'\]\s*=\s*True", "# DEBUG wird jetzt über Konfigurationsdateien gesteuert", new_content)
        new_content = re.sub(r"app\.debug\s*=\s*True", "# DEBUG wird jetzt über Konfigurationsdateien gesteuert", new_content)
        
        # Ersetzen des Secret Keys in der app.py
        new_content = re.sub(r"app\.secret_key\s*=\s*.*", "# Secret Key wird jetzt über Konfigurationsdateien gesteuert", new_content)
        new_content = re.sub(r"app\.config\['SECRET_KEY'\]\s*=\s*.*", "# Secret Key wird jetzt über Konfigurationsdateien gesteuert", new_content)
        
        # Ersetzen des direkten app.run()-Aufrufs, um Umgebungsvariablen zu berücksichtigen
        if "if __name__ == '__main__':" in new_content:
            main_pattern = r"if __name__ == '__main__':(.*?)(?=$)"
            main_section = re.search(main_pattern, new_content, re.DOTALL)
            
            if main_section:
                main_text = main_section.group(1)
                
                # Neuer main-Abschnitt mit Umgebungskonfiguration
                new_main = """
    # In der Produktionsumgebung sollte ein WSGI-Server wie Gunicorn oder uWSGI verwendet werden
    # Für die Entwicklung kann der integrierte Server verwendet werden
    port = int(os.environ.get('PORT', 5002))
    
    if os.environ.get('FLASK_ENV') == 'production':
        # Im Produktionsmodus nur auf localhost hören und SSL aktivieren, wenn verfügbar
        ssl_context = None
        if os.path.exists('cert.pem') and os.path.exists('key.pem'):
            ssl_context = ('cert.pem', 'key.pem')
        app.run(host='127.0.0.1', port=port, ssl_context=ssl_context)
    else:
        # Im Entwicklungsmodus mit aktiviertem Debug-Modus
        app.run(host='127.0.0.1', port=port, debug=True)
"""
                new_content = new_content.replace(main_text, new_main)
        
        # Überprüfen, ob os bereits importiert wurde
        if "import os" not in new_content:
            # Importanweisungen finden
            import_section = re.search(r'^(import [^\n]+|from [^\n]+)+', new_content)
            if import_section:
                # os zum Import hinzufügen
                import_end = import_section.end()
                new_content = new_content[:import_end] + "\nimport os" + new_content[import_end:]
        
        # Speichere die geänderte Datei
        with open(app_py_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        log_message("app.py wurde erfolgreich für die Verwendung von Konfigurationsdateien modifiziert.")
        return True
    
    except Exception as e:
        log_message(f"Fehler beim Modifizieren von app.py: {str(e)}")
        return False

def create_wsgi_file():
    """Erstellt eine WSGI-Datei für die Produktion"""
    wsgi_content = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
WSGI-Einstiegspunkt für Produktionsserver wie Gunicorn oder uWSGI.
'''

import os
import sys

# Setze die Umgebungsvariablen für die Produktion
os.environ['FLASK_ENV'] = 'production'

# Füge das aktuelle Verzeichnis zum Pfad hinzu
sys.path.insert(0, os.path.dirname(__file__))

# Importiere die Flask-App
from app import app as application

if __name__ == "__main__":
    # Bei direktem Aufruf die App starten
    application.run()
"""
    
    with open('wsgi.py', 'w') as f:
        f.write(wsgi_content)
    
    log_message("WSGI-Einstiegspunkt erstellt: wsgi.py")
    return True

def create_gunicorn_config():
    """Erstellt eine Gunicorn-Konfigurationsdatei"""
    gunicorn_content = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Gunicorn-Konfigurationsdatei für die Produktionsumgebung.
'''

import multiprocessing
import os

# Setze die Umgebungsvariablen für die Produktion
os.environ['FLASK_ENV'] = 'production'

# Anzahl der Worker (2-4 x Anzahl der Kerne)
workers = multiprocessing.cpu_count() * 2 + 1

# Worker-Klasse
worker_class = 'sync'

# Binde an localhost
bind = '127.0.0.1:5002'

# Arbeitsverzeichnis
chdir = os.path.dirname(__file__)

# Maximale Anzahl gleichzeitiger Clients
max_requests = 1000

# Zufällige Variation für max_requests
max_requests_jitter = 50

# Timeout-Einstellungen
timeout = 30
keepalive = 2

# Protokollierung
loglevel = 'info'
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'

# Stelle sicher, dass das Log-Verzeichnis existiert
os.makedirs('logs', exist_ok=True)

# Stille Protokollierung für die Gesundheitsprüfung
accesslog_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Sicherheitseinstellungen
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
"""
    
    # Stelle sicher, dass das Verzeichnis existiert
    os.makedirs('logs', exist_ok=True)
    
    with open('gunicorn_config.py', 'w') as f:
        f.write(gunicorn_content)
    
    log_message("Gunicorn-Konfigurationsdatei erstellt: gunicorn_config.py")
    return True

def create_startup_scripts():
    """Erstellt Startskripte für Entwicklung und Produktion"""
    
    # Entwicklungs-Startskript
    dev_script = """#!/bin/bash

# Entwicklungs-Startskript

# Umgebungsvariablen setzen
export FLASK_ENV=development
export FLASK_APP=app.py

# Flask-Server starten
python app.py
"""
    
    # Produktions-Startskript mit Gunicorn
    prod_script = """#!/bin/bash

# Produktions-Startskript

# Umgebungsvariablen setzen
export FLASK_ENV=production
export FLASK_APP=app.py

# Stellen Sie sicher, dass Gunicorn installiert ist
if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn ist nicht installiert. Installation..."
    pip install gunicorn
fi

# Gunicorn-Server mit Konfiguration starten
gunicorn -c gunicorn_config.py wsgi:application
"""
    
    # Windows-Entwicklungs-Startskript
    win_dev_script = """@echo off
REM Entwicklungs-Startskript für Windows

REM Umgebungsvariablen setzen
set FLASK_ENV=development
set FLASK_APP=app.py

REM Flask-Server starten
python app.py
"""
    
    # Windows-Produktions-Startskript
    win_prod_script = """@echo off
REM Produktions-Startskript für Windows

REM Umgebungsvariablen setzen
set FLASK_ENV=production
set FLASK_APP=app.py

REM Überprüfen, ob Waitress installiert ist (Alternative zu Gunicorn für Windows)
pip show waitress > nul 2>&1
if %errorlevel% neq 0 (
    echo Waitress ist nicht installiert. Installation...
    pip install waitress
)

REM Waitress-Server starten
python -m waitress --listen=127.0.0.1:5002 wsgi:application
"""
    
    # Unix-Skripte speichern
    with open('run_dev.sh', 'w', newline='\n') as f:
        f.write(dev_script)
    
    with open('run_prod.sh', 'w', newline='\n') as f:
        f.write(prod_script)
    
    # Windows-Skripte speichern
    with open('run_dev.bat', 'w') as f:
        f.write(win_dev_script)
    
    with open('run_prod.bat', 'w') as f:
        f.write(win_prod_script)
    
    # Ausführungsrechte für Unix-Skripte setzen (falls unter Unix)
    try:
        os.chmod('run_dev.sh', 0o755)
        os.chmod('run_prod.sh', 0o755)
    except:
        pass
    
    log_message("Startskripte erstellt: run_dev.sh, run_prod.sh, run_dev.bat, run_prod.bat")
    return True

def update_readme():
    """Aktualisiert die README mit Informationen zur Produktionsbereitstellung"""
    readme_path = 'README.md'
    
    deployment_info = """
## Bereitstellung in der Produktion

Für eine sichere Bereitstellung in der Produktionsumgebung beachten Sie bitte die folgenden Schritte:

### 1. Konfiguration

Die Anwendung verwendet separate Konfigurationsdateien für Entwicklung und Produktion:
- `instance/development.cfg`: Konfiguration für die lokale Entwicklung
- `instance/production.cfg`: Konfiguration für die Produktionsumgebung

**Wichtig:** Überprüfen Sie die Produktionskonfiguration und passen Sie sie an Ihre Umgebung an.

### 2. Starten der Anwendung

#### Entwicklung
Verwenden Sie das Skript `run_dev.sh` (Linux/Mac) oder `run_dev.bat` (Windows), um die Anwendung im Entwicklungsmodus zu starten.

#### Produktion
Verwenden Sie das Skript `run_prod.sh` (Linux/Mac) oder `run_prod.bat` (Windows), um die Anwendung im Produktionsmodus zu starten.

Im Produktionsmodus wird die Anwendung mit einem WSGI-Server (Gunicorn unter Linux/Mac, Waitress unter Windows) ausgeführt, 
was eine bessere Leistung und Sicherheit bietet als der integrierte Entwicklungsserver von Flask.

### 3. Sicherheitshinweise

- Der Debug-Modus ist in der Produktionsumgebung deaktiviert.
- Verwenden Sie in der Produktion immer HTTPS. Platzieren Sie die SSL-Zertifikate (`cert.pem` und `key.pem`) im Hauptverzeichnis.
- Regelmäßige Updates aller Abhängigkeiten durchführen, um Sicherheitslücken zu schließen.
- Alle Sicherheitsfunktionen in der Anwendung aktiviert lassen.
- Sehen Sie die Datei `SECURITY.md` für weitere Sicherheitsempfehlungen.

"""
    
    if os.path.exists(readme_path):
        # README aktualisieren
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "## Bereitstellung in der Produktion" not in content:
            with open(readme_path, 'a', encoding='utf-8') as f:
                f.write(deployment_info)
            
            log_message("README.md mit Informationen zur Produktionsbereitstellung aktualisiert.")
        else:
            log_message("README.md enthält bereits Informationen zur Produktionsbereitstellung.")
    else:
        # Neue README erstellen
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("# Alas Restaurant\n\n")
            f.write("Eine sichere Webanwendung für die Verwaltung eines Restaurants.\n\n")
            f.write(deployment_info)
        
        log_message("Neue README.md mit Informationen zur Produktionsbereitstellung erstellt.")
    
    return True

def update_requirements():
    """Aktualisiert die requirements.txt mit WSGI-Server-Abhängigkeiten"""
    req_path = 'requirements.txt'
    
    wsgi_requirements = """
# WSGI-Server für die Produktion
gunicorn==20.1.0; sys_platform != 'win32'
waitress==2.0.0; sys_platform == 'win32'
"""
    
    if os.path.exists(req_path):
        # requirements.txt aktualisieren
        with open(req_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "gunicorn" not in content and "waitress" not in content:
            with open(req_path, 'a', encoding='utf-8') as f:
                f.write(wsgi_requirements)
            
            log_message("requirements.txt mit WSGI-Server-Abhängigkeiten aktualisiert.")
        else:
            log_message("requirements.txt enthält bereits WSGI-Server-Abhängigkeiten.")
    else:
        # Neue requirements.txt erstellen
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write("# Hauptabhängigkeiten\n")
            f.write("flask==2.0.1\n")
            f.write("flask-wtf==0.15.1\n")
            f.write("werkzeug==2.0.1\n")
            f.write(wsgi_requirements)
        
        log_message("Neue requirements.txt mit WSGI-Server-Abhängigkeiten erstellt.")
    
    return True

if __name__ == "__main__":
    log_message("Starte Produktionskonfiguration und Deaktivierung des Debug-Modus...")
    
    # Konfigurationsdateien erstellen
    create_config_files()
    
    # app.py für die Verwendung von Konfigurationsdateien modifizieren
    modify_app_py_for_config()
    
    # WSGI-Datei erstellen
    create_wsgi_file()
    
    # Gunicorn-Konfiguration erstellen
    create_gunicorn_config()
    
    # Startskripte erstellen
    create_startup_scripts()
    
    # README aktualisieren
    update_readme()
    
    # requirements.txt aktualisieren
    update_requirements()
    
    log_message("Produktionskonfiguration und Deaktivierung des Debug-Modus abgeschlossen.")
    log_message("Die Anwendung kann jetzt sicher in einer Produktionsumgebung bereitgestellt werden.")
    log_message("Verwenden Sie die Startskripte run_dev.sh/bat für die Entwicklung und run_prod.sh/bat für die Produktion.") 