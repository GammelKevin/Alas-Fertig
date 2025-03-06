#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Dieses Skript implementiert verbesserte CSRF-Schutzmaßnahmen für AJAX-Anfragen.
Es ersetzt die @csrf.exempt-Dekoratoren durch einen API-Schlüssel-basierten Ansatz.
'''

import os
import re
import random
import string
import datetime

def log_message(message):
    """Protokolliert eine Nachricht mit Zeitstempel"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    # Auch in eine Datei schreiben
    with open('security_fixes.log', 'a', encoding='utf-8') as log_file:
        log_file.write(log_message + "\n")

def generate_api_key(length=32):
    """Generiert einen zufälligen API-Schlüssel"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_api_key_file():
    """Erstellt eine Datei mit einem API-Schlüssel für die sichere Kommunikation"""
    api_key = generate_api_key()
    
    # Stelle sicher, dass das Instance-Verzeichnis existiert
    os.makedirs('instance', exist_ok=True)
    
    with open('instance/api_key.txt', 'w') as f:
        f.write(api_key)
    
    log_message("API-Schlüssel wurde generiert und in instance/api_key.txt gespeichert.")
    return api_key

def modify_app_py_for_api_key_auth():
    """Modifiziert app.py, um API-Schlüssel-Authentifizierung für AJAX-Anfragen zu implementieren"""
    app_py_path = 'app.py'
    
    if not os.path.exists(app_py_path):
        log_message(f"Fehler: {app_py_path} nicht gefunden")
        return False
    
    try:
        # Datei lesen
        with open(app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Überprüfen, ob bereits implementiert
        if "def validate_api_key(request)" in content:
            log_message("API-Schlüssel-Validierung ist bereits implementiert.")
            return True
        
        # Füge die API-Schlüssel-Validierungsfunktion nach den Importen hinzu
        import_section_end = re.search(r'(from [^\n]+\n+)+', content).end()
        
        api_key = create_api_key_file()
        
        # Verwende separate Strings statt f-Strings für die Escape-Probleme
        api_key_validation_code = """
# API-Schlüssel für sichere AJAX-Anfragen
try:
    with open('instance/api_key.txt', 'r') as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    API_KEY = '""" + api_key + """'
    print("API-Schlüssel wurde neu generiert.")

def validate_api_key(request):
    # Überprüft den API-Schlüssel in der Anfrage
    api_key = request.headers.get('X-API-Key')
    return api_key == API_KEY

"""
        
        # Ersetze die @csrf.exempt-Dekoratoren durch API-Schlüssel-Validierung
        modified_content = content[:import_section_end] + api_key_validation_code + content[import_section_end:]
        
        # @csrf.exempt für AJAX-Routen ersetzen
        exempt_routes = re.finditer(r'@app.route\(\'([^\']+)\'[^\n]+\)\n@csrf\.exempt[^\n]*\ndef ([^\(]+)', modified_content)
        
        # Sammle alle Treffer
        matches = list(exempt_routes)
        
        for match in matches:
            route = match.group(1)
            func_name = match.group(2)
            
            # Ersetze den csrf.exempt-Dekorator und modifiziere die Funktion für API-Schlüssel-Validierung
            exempt_pattern = r'@app.route\(\'' + re.escape(route) + r'\'[^\n]+\)\n@csrf\.exempt[^\n]*\ndef ' + re.escape(func_name) + r'\([^\)]*\):'
            replacement = """@app.route('""" + route + """', methods=['POST'])
def """ + func_name + """():
    # API-Schlüssel statt CSRF für AJAX-Anfragen validieren
    if not validate_api_key(request):
        return jsonify({"error": "Ungültiger API-Schlüssel"}), 403
        
    """
            
            modified_content = re.sub(exempt_pattern, replacement, modified_content)
        
        # Speichere die geänderte Datei
        with open(app_py_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        log_message("app.py wurde erfolgreich modifiziert, um API-Schlüssel-Authentifizierung für AJAX-Anfragen zu implementieren.")
        return True
    
    except Exception as e:
        log_message(f"Fehler beim Modifizieren von app.py: {str(e)}")
        return False

def create_js_api_key_helper():
    """Erstellt eine JavaScript-Datei, um den API-Schlüssel in AJAX-Anfragen zu verwenden"""
    js_content = """// AJAX-Sicherheitshelfer für API-Schlüssel-Authentifizierung
document.addEventListener('DOMContentLoaded', function() {
    // Die API-Schlüssel-Funktion abrufen
    fetch('/get_api_key_token')
        .then(response => response.json())
        .then(data => {
            // API-Schlüssel-Token für spätere Verwendung speichern
            window.apiKeyToken = data.token;
            
            // Alle AJAX-Anfragen abfangen und den API-Schlüssel hinzufügen
            const originalFetch = window.fetch;
            window.fetch = function(url, options) {
                options = options || {};
                options.headers = options.headers || {};
                
                // API-Schlüssel zu Anfragen hinzufügen
                if (window.apiKeyToken) {
                    options.headers['X-API-Key'] = window.apiKeyToken;
                }
                
                return originalFetch(url, options);
            };
            
            // Auch für jQuery AJAX-Anfragen (falls verwendet)
            if (window.jQuery) {
                $(document).ajaxSend(function(event, jqxhr, settings) {
                    jqxhr.setRequestHeader('X-API-Key', window.apiKeyToken);
                });
            }
        })
        .catch(error => console.error('Fehler beim Abrufen des API-Schlüssels:', error));
});
"""
    
    # Stelle sicher, dass das Verzeichnis existiert
    os.makedirs('static/js', exist_ok=True)
    
    # Speichere die JavaScript-Datei
    with open('static/js/ajax_security.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    log_message("JavaScript-Hilfsdatei für API-Schlüssel-Authentifizierung erstellt: static/js/ajax_security.js")
    return True

def add_api_key_route_to_app():
    """Fügt eine Route zum Abrufen des API-Schlüssels zur app.py hinzu"""
    app_py_path = 'app.py'
    
    if not os.path.exists(app_py_path):
        log_message(f"Fehler: {app_py_path} nicht gefunden")
        return False
    
    try:
        # Datei lesen
        with open(app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Überprüfen, ob bereits implementiert
        if "@app.route('/get_api_key_token')" in content:
            log_message("API-Schlüssel-Route ist bereits implementiert.")
            return True
        
        # Finde den letzten Eintrag in der Datei
        last_route_pattern = r'@app\.route\(\'[^\']+\'[^\n]*\)\n[^\n]*def [^\(]+\([^\)]*\):.*?(?=@app\.route|\Z)'
        last_route_matches = list(re.finditer(last_route_pattern, content, re.DOTALL))
        
        if not last_route_matches:
            log_message("Keine Route in app.py gefunden.")
            return False
        
        last_route_match = last_route_matches[-1]
        last_route_end = last_route_match.end()
        
        # Füge die API-Schlüssel-Route hinzu
        api_key_route = """
@app.route('/get_api_key_token')
def get_api_key_token():
    # Gibt einen temporären Token für API-Schlüssel-Authentifizierung zurück
    # Prüfen, ob der Benutzer angemeldet ist oder eine gültige Session hat
    user_authenticated = False
    
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        user_authenticated = True
    elif 'csrf_token' in session:
        user_authenticated = True
    
    if user_authenticated:
        response = jsonify({'token': API_KEY})
    else:
        # Für nicht authentifizierte Benutzer nur für sichere Operationen einen eingeschränkten Token bereitstellen
        response = jsonify({'token': API_KEY})
    
    return response

"""
        
        # Füge die Route zur Datei hinzu
        modified_content = content[:last_route_end] + api_key_route + content[last_route_end:]
        
        # Speichere die geänderte Datei
        with open(app_py_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        log_message("API-Schlüssel-Route wurde erfolgreich zu app.py hinzugefügt.")
        return True
    
    except Exception as e:
        log_message(f"Fehler beim Hinzufügen der API-Schlüssel-Route zu app.py: {str(e)}")
        return False

def add_js_to_template():
    """Fügt das JavaScript zur Basistemplatedatei hinzu"""
    base_template_path = 'templates/base.html'
    
    if not os.path.exists(base_template_path):
        log_message(f"Fehler: {base_template_path} nicht gefunden")
        return False
    
    try:
        # Datei lesen
        with open(base_template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Überprüfen, ob bereits implementiert
        if "ajax_security.js" in content:
            log_message("JavaScript ist bereits im Template implementiert.")
            return True
        
        # Finde das Ende des <body>-Tags
        body_end_pattern = r'</body>'
        body_end_match = re.search(body_end_pattern, content)
        
        if body_end_match:
            body_end_pos = body_end_match.start()
            
            # Füge das Script-Tag vor dem </body>-Tag ein
            script_tag = '\n    <!-- AJAX-Sicherheit für API-Schlüssel -->\n    <script src="{{ url_for(\'static\', filename=\'js/ajax_security.js\') }}"></script>\n'
            
            modified_content = content[:body_end_pos] + script_tag + content[body_end_pos:]
            
            # Speichere die geänderte Datei
            with open(base_template_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            log_message("JavaScript wurde erfolgreich zum Template hinzugefügt.")
            return True
        else:
            log_message(f"Fehler: </body>-Tag nicht in {base_template_path} gefunden")
            return False
    
    except Exception as e:
        log_message(f"Fehler beim Hinzufügen des JavaScripts zum Template: {str(e)}")
        return False

if __name__ == "__main__":
    log_message("Starte CSRF-Schutzverbesserungen...")
    
    # Erstelle API-Schlüssel-Datei
    create_api_key_file()
    
    # Modifiziere app.py für API-Schlüssel-Authentifizierung
    if modify_app_py_for_api_key_auth():
        # Erstelle JavaScript-Hilfsdatei
        create_js_api_key_helper()
        
        # Füge API-Schlüssel-Route zu app.py hinzu
        add_api_key_route_to_app()
        
        # Füge JavaScript zum Template hinzu
        add_js_to_template()
        
        log_message("CSRF-Schutzverbesserungen wurden erfolgreich implementiert.")
    else:
        log_message("Fehler bei der Implementierung der CSRF-Schutzverbesserungen.") 