# Sicherheitsmaßnahmen für die Alas Restaurant Webseite

Dieses Dokument enthält wichtige Informationen zur Sicherheit der Alas Restaurant Webseite und beschreibt die implementierten Schutzmaßnahmen sowie bewährte Praktiken für die Wartung und Weiterentwicklung.

## Implementierte Sicherheitsmaßnahmen

### XSS-Schutz (Cross-Site Scripting)
- Alle Benutzereingaben werden durch die Funktion `sanitize_html()` gereinigt, bevor sie in der Datenbank gespeichert werden
- Jinja2-Templates maskieren HTML-Zeichen standardmäßig
- Die Bibliothek "bleach" wird verwendet, um bösartigen HTML-Code in Texteingaben zu entfernen

### CSRF-Schutz (Cross-Site Request Forgery)
- Alle Formulare enthalten CSRF-Token (durch Flask-WTF)
- AJAX-Anfragen müssen CSRF-Token im Header mitschicken
- Für sensitive Aktionen werden zusätzliche Bestätigungen erzwungen

### SQL-Injection-Schutz
- Verwendung von SQLAlchemy ORM verhindert die meisten SQL-Injection-Angriffe
- Parameterisierte Abfragen werden für alle direkten Datenbankzugriffe verwendet
- Validierung aller Eingaben, die in Datenbankabfragen verwendet werden

### Dateiupload-Sicherheit
- Strenge Validierung der hochgeladenen Dateitypen (Dateiendung und MIME-Typ)
- Überprüfung des Dateiinhalts auf Übereinstimmung mit dem deklarierten Typ
- Sichere Generierung von Dateinamen mit Zeitstempeln
- Beschränkung der Dateigröße und -typen auf das Notwendige

### Authentifizierung und Autorisierung
- Passwörter werden mit sicheren Hashing-Algorithmen gespeichert
- Anmeldeversuche werden protokolliert und bei Verdacht auf Brute-Force-Angriffe begrenzt
- Admin-Bereiche sind durch Anmeldung und Rollenzuweisung geschützt

## Sicherheits-Tools und -Skripte

Dieses Projekt enthält mehrere Tools zur Überprüfung und Verbesserung der Sicherheit:

1. **security_utils.py**: Enthält Hilfsfunktionen für die Eingabevalidierung und -bereinigung
2. **scan_uploads.py**: Überprüft Upload-Verzeichnisse auf potenziell gefährliche Dateien
3. **check_sql_injection.py**: Scannt den Code auf mögliche SQL-Injection-Schwachstellen

## Sicherheitsempfehlungen für die Weiterentwicklung

1. **Eingabevalidierung**: Validieren Sie **ALLE** Benutzereingaben, bevor sie verarbeitet werden
2. **Output-Encoding**: Stellen Sie sicher, dass alle Daten ordnungsgemäß maskiert werden, bevor sie in HTML ausgegeben werden
3. **Datei-Uploads**: Seien Sie besonders vorsichtig mit Datei-Uploads und überprüfen Sie immer den Inhalt
4. **Drittanbieter-Bibliotheken**: Halten Sie alle Abhängigkeiten auf dem neuesten Stand
5. **Sicherheitstests**: Führen Sie regelmäßig Sicherheitstests durch und verwenden Sie Tools wie OWASP ZAP oder Burp Suite

## Installation der Sicherheitskomponenten

Um alle Sicherheitskomponenten zu installieren, führen Sie den folgenden Befehl aus:

```
pip install -r security_requirements.txt
```

## Regelmäßige Sicherheitsüberprüfungen

Es wird empfohlen, regelmäßige Sicherheitsüberprüfungen durchzuführen:

1. Führen Sie `scan_uploads.py` aus, um das Upload-Verzeichnis zu überprüfen
2. Führen Sie `check_sql_injection.py` aus, um den Code auf SQL-Injection-Schwachstellen zu scannen
3. Überprüfen Sie die Logs auf verdächtige Aktivitäten
4. Aktualisieren Sie regelmäßig alle Abhängigkeiten

## Sicherheitslücken melden

Wenn Sie eine Sicherheitslücke in der Alas Restaurant Webseite entdecken, melden Sie diese bitte direkt an die Administratoren oder das Entwicklungsteam.

---

*Dieses Dokument sollte regelmäßig überprüft und aktualisiert werden, um die Sicherheit der Webseite zu gewährleisten.* 