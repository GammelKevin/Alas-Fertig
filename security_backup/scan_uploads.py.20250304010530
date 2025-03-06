"""
Upload-Scanner - Überprüft alle hochgeladenen Dateien auf Sicherheitsrisiken.

Dieses Skript durchsucht das Upload-Verzeichnis und überprüft alle Dateien 
auf potenziell gefährliche Inhalte oder ungültige MIME-Typen.

Es kann als eigenständiges Skript ausgeführt oder in die Hauptanwendung integriert werden.
"""

import os
import sys
import magic
from datetime import datetime
from PIL import Image
import imghdr

# Konfiguration
UPLOAD_FOLDER = 'static/uploads'
QUARANTINE_FOLDER = 'static/quarantine'
LOG_FILE = 'upload_scan.log'
ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp'
}

def setup_folders():
    """Erstellt die erforderlichen Verzeichnisse, falls sie nicht existieren."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(QUARANTINE_FOLDER, exist_ok=True)
    
    # Galerie-Unterverzeichnis
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'gallery'), exist_ok=True)
    
    # Menü-Unterverzeichnis
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'menu'), exist_ok=True)
    
    print(f"Verzeichnisse überprüft: {UPLOAD_FOLDER}, {QUARANTINE_FOLDER}")

def log_message(message):
    """Schreibt eine Nachricht in die Protokolldatei."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def validate_image(file_path):
    """
    Überprüft, ob eine Datei ein gültiges Bild ist.
    
    Args:
        file_path: Der Pfad zur zu überprüfenden Datei
        
    Returns:
        bool: True, wenn die Datei ein gültiges Bild ist, sonst False
    """
    try:
        # Überprüfe MIME-Typ mit python-magic
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        if file_type not in ALLOWED_MIME_TYPES:
            return False
        
        # Versuche, das Bild mit PIL zu öffnen
        img = Image.open(file_path)
        img.verify()  # Überprüft, ob das Bild intakt ist
        
        # Zusätzliche Validierung mit imghdr
        detected_format = imghdr.what(file_path)
        if detected_format not in ['jpeg', 'png', 'gif', 'webp']:
            return False
            
        return True
    except Exception as e:
        log_message(f"Fehler bei der Bildvalidierung für {file_path}: {str(e)}")
        return False

def quarantine_file(file_path):
    """
    Verschiebt eine verdächtige Datei in Quarantäne.
    
    Args:
        file_path: Der Pfad zur zu quarantänierenden Datei
    """
    try:
        filename = os.path.basename(file_path)
        quarantine_path = os.path.join(QUARANTINE_FOLDER, filename)
        
        # Falls die Datei bereits existiert, Timestamp hinzufügen
        if os.path.exists(quarantine_path):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            name, ext = os.path.splitext(filename)
            quarantine_path = os.path.join(QUARANTINE_FOLDER, f"{name}_{timestamp}{ext}")
        
        # Datei in Quarantäne verschieben
        os.rename(file_path, quarantine_path)
        log_message(f"Datei in Quarantäne verschoben: {file_path} -> {quarantine_path}")
        print(f"Potentiell unsichere Datei in Quarantäne verschoben: {filename}")
    except Exception as e:
        log_message(f"Fehler beim Verschieben der Datei {file_path} in Quarantäne: {str(e)}")
        print(f"Fehler: {str(e)}")

def scan_directory(directory):
    """
    Durchsucht ein Verzeichnis nach Dateien und überprüft sie.
    
    Args:
        directory: Das zu durchsuchende Verzeichnis
    """
    print(f"Scanne Verzeichnis: {directory}")
    log_message(f"Starte Scan des Verzeichnisses: {directory}")
    
    unsafe_files = 0
    total_files = 0
    
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            total_files += 1
            
            # Nur Bilddateien überprüfen
            if not validate_image(file_path):
                log_message(f"Unsichere Datei gefunden: {file_path}")
                quarantine_file(file_path)
                unsafe_files += 1
    
    log_message(f"Scan abgeschlossen. {unsafe_files} von {total_files} Dateien wurden in Quarantäne verschoben.")
    print(f"Scan abgeschlossen: {unsafe_files} von {total_files} Dateien als unsicher eingestuft.")

def main():
    """Hauptfunktion des Upload-Scanners."""
    print("Alas Restaurant Upload-Scanner")
    print("------------------------------")
    
    setup_folders()
    
    # Beginne mit dem Scan
    scan_directory(UPLOAD_FOLDER)
    
    print("Scan abgeschlossen. Siehe Protokoll für Details.")

if __name__ == "__main__":
    main() 