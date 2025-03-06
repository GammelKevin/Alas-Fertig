"""
SQL-Injection-Checker für Alas Restaurant Webseite

Dieses Skript überprüft die Codebasis auf mögliche SQL-Injection-Schwachstellen.
Es wird in der Entwicklungsphase verwendet, um potenzielle Sicherheitsrisiken zu identifizieren.

Hinweis: Dieses Skript ist keine umfassende Sicherheitsanalyse und ersetzt keine professionelle 
Sicherheitsüberprüfung. Es dient lediglich als Hilfsmittel zur frühzeitigen Erkennung
offensichtlicher Probleme.
"""

import os
import re
import sys
from datetime import datetime

# Standardpfade für die Überprüfung
DEFAULT_PATHS = [
    'app.py',
    'admin_routes.py',
    'utils.py'
]

# Muster, die auf unsichere SQL-Operationen hindeuten könnten
UNSAFE_PATTERNS = [
    r'execute\(\s*".*?\%.*?\)',  # Unsicheres Parametrisieren mit %
    r'execute\(\s*".*?\{.*?\}.*?\)(?!\s*\.format\()',  # Unsicheres String Formatting
    r'execute\(\s*".*?\$.*?\)',  # String Interpolation in SQL
    r'execute\(\s*".*?"\s*\+\s*.+?\)',  # Stringverkettung in SQL-Abfrage
    r'execute\(\s*f"[^"]*?{[^}]*?}[^"]*?"',  # f-String in SQL-Query (potentiell gefährlich)
    r'text\(\s*".*?"\s*\+\s*.+?\)',  # Stringverkettung in SQLAlchemy Text
]

# Muster für sichere Praktiken
SAFE_PATTERNS = [
    r'execute\(\s*".*?"\s*,\s*\(.+?\)\s*\)',  # Parameterisierte Query (sicher)
    r'execute\(\s*text\(".*?"\)\s*,\s*\{.+?\}\s*\)',  # SQLAlchemy text() mit Parametern
]

def scan_file(file_path):
    """
    Scannt eine Datei nach potenziellen SQL-Injection-Schwachstellen.
    
    Args:
        file_path: Der Pfad zur zu scannenden Datei
        
    Returns:
        list: Eine Liste der gefundenen problematischen Codezeilen
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = content.split('\n')
        issues = []
        
        for i, line in enumerate(lines):
            line_number = i + 1
            
            # Prüfe auf unsichere Muster
            for pattern in UNSAFE_PATTERNS:
                if re.search(pattern, line):
                    # Überprüfe, ob es sich um ein sicheres Muster handelt
                    is_safe = any(re.search(safe_pattern, line) for safe_pattern in SAFE_PATTERNS)
                    
                    if not is_safe:
                        issues.append({
                            'line_number': line_number,
                            'line': line.strip(),
                            'file': file_path
                        })
        
        return issues
    
    except Exception as e:
        print(f"Fehler beim Scannen von {file_path}: {str(e)}")
        return []

def generate_report(issues):
    """
    Erstellt einen Bericht über gefundene Probleme.
    
    Args:
        issues: Eine Liste der gefundenen Probleme
        
    Returns:
        str: Ein Bericht als formatierter String
    """
    if not issues:
        return "Keine potenziellen SQL-Injection-Schwachstellen gefunden.\n"
    
    report = f"Potenziell unsichere SQL-Operationen gefunden: {len(issues)}\n"
    report += "=" * 80 + "\n\n"
    
    for issue in issues:
        report += f"Datei: {issue['file']}\n"
        report += f"Zeile: {issue['line_number']}\n"
        report += f"Code: {issue['line']}\n"
        report += "-" * 80 + "\n"
    
    report += "\n"
    report += "Hinweis: Dies ist eine automatisierte Überprüfung, die zu falschen Ergebnissen führen kann.\n"
    report += "Jede identifizierte Zeile sollte manuell überprüft werden.\n"
    
    return report

def save_report(report, output_file='sql_injection_report.txt'):
    """
    Speichert den Bericht in einer Datei.
    
    Args:
        report: Der zu speichernde Bericht
        output_file: Der Pfad zur Ausgabedatei
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"SQL-Injection-Überprüfung - {timestamp}\n")
        f.write("=" * 80 + "\n\n")
        f.write(report)
    
    print(f"Bericht gespeichert in {output_file}")

def scan_directory(dir_path):
    """
    Durchsucht ein Verzeichnis nach Python-Dateien und scannt sie.
    
    Args:
        dir_path: Der Pfad zum zu durchsuchenden Verzeichnis
        
    Returns:
        list: Eine Liste der gefundenen Probleme
    """
    all_issues = []
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                issues = scan_file(file_path)
                all_issues.extend(issues)
    
    return all_issues

def main():
    """Hauptfunktion des SQL-Injection-Checkers."""
    print("SQL-Injection-Checker für Alas Restaurant")
    print("=" * 40)
    
    # Scanne die Standardpfade
    all_issues = []
    for path in DEFAULT_PATHS:
        if os.path.isfile(path):
            print(f"Scanne Datei: {path}")
            issues = scan_file(path)
            all_issues.extend(issues)
        elif os.path.isdir(path):
            print(f"Scanne Verzeichnis: {path}")
            issues = scan_directory(path)
            all_issues.extend(issues)
    
    # Erstelle und speichere den Bericht
    report = generate_report(all_issues)
    save_report(report)
    
    # Zeige eine Zusammenfassung an
    print(f"\nÜberprüfung abgeschlossen: {len(all_issues)} potenzielle Probleme gefunden.")

if __name__ == "__main__":
    main() 