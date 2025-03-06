"""
Sicherheits-Setup-Skript für Alas Restaurant Webseite

Dieses Skript installiert und konfiguriert alle notwendigen Sicherheitskomponenten
für die Alas Restaurant Webseite. Es führt folgende Aktionen aus:

1. Installation der benötigten Sicherheits-Pakete
2. Überprüfung der Verzeichnisstrukturen und Berechtigungen
3. Initialisierung der Sicherheitsmodule
4. Durchführung eines ersten Sicherheits-Scans

Verwendung:
python setup_security.py
"""

import os
import sys
import subprocess
import platform
import shutil
from datetime import datetime

def log_message(message, log_file="security_setup.log"):
    """Schreibt eine Nachricht in die Log-Datei und gibt sie auf der Konsole aus."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    print(log_entry)
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def install_requirements():
    """Installiert die benötigten Sicherheits-Pakete."""
    log_message("Installiere Sicherheits-Abhängigkeiten...")
    
    try:
        # Verwende pip zur Installation der Anforderungen
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "security_requirements.txt"])
        log_message("Sicherheitsabhängigkeiten erfolgreich installiert.")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"Fehler bei der Installation der Abhängigkeiten: {str(e)}")
        return False

def check_directory_structure():
    """Überprüft und erstellt die notwendigen Verzeichnisse."""
    log_message("Überprüfe Verzeichnisstruktur...")
    
    required_dirs = [
        "static/uploads",
        "static/uploads/gallery",
        "static/uploads/menu",
        "static/quarantine"
    ]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            log_message(f"Verzeichnis erstellt: {directory}")
        else:
            log_message(f"Verzeichnis existiert bereits: {directory}")
    
    # Überprüfe Berechtigungen für Windows
    if platform.system() == "Windows":
        try:
            # In Windows können wir nur begrenzt mit Berechtigungen umgehen
            log_message("Windows-System erkannt. Überprüfung der Berechtigungen nicht erforderlich.")
        except Exception as e:
            log_message(f"Warnung bei der Überprüfung der Berechtigungen: {str(e)}")
    # Für Unix-Systeme
    else:
        try:
            for directory in required_dirs:
                os.chmod(directory, 0o755)  # rwxr-xr-x
            log_message("Berechtigungen für Verzeichnisse konfiguriert.")
        except Exception as e:
            log_message(f"Fehler bei der Konfiguration der Berechtigungen: {str(e)}")

def initialize_security_modules():
    """Initialisiert die Sicherheitsmodule durch Überprüfung ihrer Funktionalität."""
    log_message("Initialisiere Sicherheitsmodule...")
    
    try:
        # Überprüfe, ob die security_utils.py-Datei existiert
        if os.path.exists("security_utils.py"):
            log_message("Sicherheitsmodul gefunden: security_utils.py")
        else:
            log_message("WARNUNG: security_utils.py nicht gefunden!")
            return False
        
        # Überprüfe, ob scan_uploads.py existiert
        if os.path.exists("scan_uploads.py"):
            log_message("Sicherheitsmodul gefunden: scan_uploads.py")
        else:
            log_message("WARNUNG: scan_uploads.py nicht gefunden!")
            return False
        
        # Überprüfe, ob check_sql_injection.py existiert
        if os.path.exists("check_sql_injection.py"):
            log_message("Sicherheitsmodul gefunden: check_sql_injection.py")
        else:
            log_message("WARNUNG: check_sql_injection.py nicht gefunden!")
            return False
        
        log_message("Alle Sicherheitsmodule initialisiert.")
        return True
        
    except Exception as e:
        log_message(f"Fehler bei der Initialisierung der Sicherheitsmodule: {str(e)}")
        return False

def run_initial_security_scan():
    """Führt einen ersten Sicherheits-Scan durch."""
    log_message("Führe initialen Sicherheits-Scan durch...")
    
    try:
        # Führe scan_uploads.py aus
        log_message("Starte Scan der hochgeladenen Dateien...")
        subprocess.check_call([sys.executable, "scan_uploads.py"])
        
        # Führe check_sql_injection.py aus
        log_message("Starte SQL-Injection-Scan...")
        subprocess.check_call([sys.executable, "check_sql_injection.py"])
        
        log_message("Initialer Sicherheits-Scan abgeschlossen.")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"Fehler beim Ausführen des Sicherheits-Scans: {str(e)}")
        return False

def create_security_backup():
    """Erstellt ein Backup der wichtigen Sicherheitsdateien."""
    log_message("Erstelle Sicherheits-Backup...")
    
    backup_dir = "security_backup"
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = [
        "security_utils.py",
        "scan_uploads.py",
        "check_sql_injection.py",
        "SECURITY.md",
        "security_requirements.txt"
    ]
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    try:
        for file in files_to_backup:
            if os.path.exists(file):
                dest = os.path.join(backup_dir, f"{file}.{timestamp}")
                shutil.copy2(file, dest)
                log_message(f"Backup erstellt: {file} -> {dest}")
        
        log_message("Sicherheits-Backup abgeschlossen.")
        return True
    except Exception as e:
        log_message(f"Fehler beim Erstellen des Backups: {str(e)}")
        return False

def main():
    """Hauptfunktion des Setup-Skripts."""
    print("===== Alas Restaurant Sicherheits-Setup =====")
    print("Installiere und konfiguriere Sicherheitskomponenten...")
    print("")
    
    # Führe alle Setup-Schritte aus
    steps = [
        (install_requirements, "Installation der Sicherheits-Abhängigkeiten"),
        (check_directory_structure, "Überprüfung der Verzeichnisstruktur"),
        (initialize_security_modules, "Initialisierung der Sicherheitsmodule"),
        (create_security_backup, "Erstellung des Sicherheits-Backups"),
        (run_initial_security_scan, "Durchführung des initialen Sicherheits-Scans")
    ]
    
    success_count = 0
    
    for step_func, step_name in steps:
        print(f"\n--- {step_name} ---")
        if step_func():
            success_count += 1
        else:
            print(f"WARNUNG: Schritt '{step_name}' wurde nicht vollständig abgeschlossen.")
    
    print("\n===== Sicherheits-Setup abgeschlossen =====")
    print(f"{success_count} von {len(steps)} Schritten erfolgreich abgeschlossen.")
    
    if success_count == len(steps):
        print("\nDie Sicherheitskonfiguration wurde erfolgreich durchgeführt!")
    else:
        print("\nDie Sicherheitskonfiguration wurde mit Warnungen abgeschlossen.")
        print("Bitte überprüfen Sie die Log-Datei 'security_setup.log' für Details.")

if __name__ == "__main__":
    main() 