#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Dieses Skript fügt die fehlende Spalte 'is_drink_category' zur menu_category-Tabelle hinzu
und aktualisiert existierende Kategorien basierend auf ihrem Namen.
'''

import os
import sqlite3
import datetime
import shutil

def log_message(message):
    """Protokolliert eine Nachricht mit Zeitstempel"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    # Auch in eine Datei schreiben
    with open('db_update.log', 'a', encoding='utf-8') as log_file:
        log_file.write(log_message + "\n")

def check_column_exists(cursor, table, column):
    """Überprüft, ob eine Spalte in einer Tabelle existiert"""
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    return column in columns

def backup_database(db_path):
    """Erstellt ein Backup der Datenbank"""
    if not os.path.exists(db_path):
        log_message(f"Datenbank nicht gefunden: {db_path}")
        return False
    
    backup_dir = 'db_backups'
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"restaurant_backup_{timestamp}.db")
    
    try:
        shutil.copy2(db_path, backup_path)
        log_message(f"Datenbank-Backup erstellt: {backup_path}")
        return True
    except Exception as e:
        log_message(f"Fehler beim Erstellen des Datenbank-Backups: {str(e)}")
        return False

def add_column_if_not_exists():
    """Fügt die 'is_drink_category'-Spalte zur Tabelle menu_category hinzu, wenn sie nicht existiert"""
    db_path = 'instance/restaurant.db'
    
    if not os.path.exists(db_path):
        log_message(f"Datenbank nicht gefunden: {db_path}")
        return False
    
    # Backup erstellen
    if not backup_database(db_path):
        log_message("Konnte kein Backup erstellen, breche ab.")
        return False
    
    try:
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Überprüfen, ob die Tabelle menu_category existiert
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='menu_category'")
        if not cursor.fetchone():
            log_message("Tabelle menu_category existiert nicht. Nichts zu tun.")
            conn.close()
            return False
        
        # Überprüfen, ob die Spalte bereits existiert
        if check_column_exists(cursor, 'menu_category', 'is_drink_category'):
            log_message("Spalte is_drink_category existiert bereits. Nichts zu tun.")
            conn.close()
            return True
        
        # Spalte hinzufügen
        log_message("Füge Spalte is_drink_category zur Tabelle menu_category hinzu...")
        cursor.execute("ALTER TABLE menu_category ADD COLUMN is_drink_category INTEGER DEFAULT 0")
        
        # Getränkekategorien identifizieren und aktualisieren
        drink_keywords = ['getränk', 'getränke', 'drink', 'drinks', 'wein', 'bier', 'saft', 'säfte', 'wasser', 'kaffee', 'tee']
        
        # Alle Kategorien abrufen
        cursor.execute("SELECT id, name FROM menu_category")
        categories = cursor.fetchall()
        
        for cat_id, cat_name in categories:
            is_drink = 0
            # Überprüfen, ob ein Schlüsselwort im Namen enthalten ist
            for keyword in drink_keywords:
                if keyword.lower() in cat_name.lower():
                    is_drink = 1
                    break
            
            # Kategorie aktualisieren
            cursor.execute("UPDATE menu_category SET is_drink_category = ? WHERE id = ?", (is_drink, cat_id))
            log_message(f"Kategorie '{cat_name}' als {'Getränk' if is_drink else 'Speise'} aktualisiert.")
        
        # Änderungen speichern
        conn.commit()
        log_message("Spalte is_drink_category erfolgreich hinzugefügt und Kategorien aktualisiert.")
        
        conn.close()
        return True
    
    except Exception as e:
        log_message(f"Fehler beim Hinzufügen der Spalte: {str(e)}")
        return False

if __name__ == "__main__":
    log_message("Starte Datenbank-Update...")
    
    if add_column_if_not_exists():
        log_message("Datenbank-Update erfolgreich abgeschlossen.")
    else:
        log_message("Datenbank-Update fehlgeschlagen.") 