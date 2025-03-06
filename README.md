# Alas Restaurant

Eine sichere Webanwendung für die Verwaltung eines Restaurants.


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

