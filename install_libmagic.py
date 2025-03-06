#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Dieses Skript installiert und konfiguriert die libmagic-Bibliothek für verschiedene Betriebssysteme.
Es behandelt das Problem mit dem fehlenden python-magic-Paket, das für Dateityp-Validierung benötigt wird.
'''

import os
import sys
import platform
import subprocess
import datetime

def log_message(message):
    """Protokolliert eine Nachricht mit Zeitstempel"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    # Auch in eine Datei schreiben
    with open('security_fixes.log', 'a', encoding='utf-8') as log_file:
        log_file.write(log_message + "\n")

def detect_os():
    """Erkennt das Betriebssystem"""
    system = platform.system().lower()
    
    if system == 'windows':
        return 'windows'
    elif system == 'darwin':
        return 'macos'
    elif system == 'linux':
        return 'linux'
    else:
        return 'unknown'

def run_command(command, shell=True):
    """Führt einen Befehl aus und gibt das Ergebnis zurück"""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def install_libmagic_windows():
    """Installiert libmagic für Windows"""
    log_message("Installation von libmagic und python-magic für Windows...")
    
    # Prüfen, ob pip verfügbar ist
    success, _ = run_command("pip --version")
    if not success:
        log_message("Fehler: pip ist nicht verfügbar. Bitte installieren Sie pip, um fortzufahren.")
        return False
    
    # Installation von python-magic-bin für Windows
    log_message("Installation von python-magic-bin...")
    success, output = run_command("pip install python-magic-bin")
    
    if not success:
        log_message(f"Fehler bei der Installation von python-magic-bin: {output}")
        return False
    
    log_message("Installation von python-magic-bin erfolgreich abgeschlossen.")
    
    # Überprüfen, ob die Installation funktioniert
    test_script = """
import magic
try:
    magic.Magic()
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {str(e)}')
"""
    
    with open('test_magic.py', 'w') as f:
        f.write(test_script)
    
    success, output = run_command("python test_magic.py")
    os.remove('test_magic.py')
    
    if 'SUCCESS' in output:
        log_message("libmagic-Test erfolgreich: Die Bibliothek funktioniert korrekt.")
        return True
    else:
        log_message(f"libmagic-Test fehlgeschlagen: {output}")
        
        # Alternatives Paket versuchen
        log_message("Versuche alternative Installation mit python-magic...")
        success, output = run_command("pip install python-magic")
        
        if not success:
            log_message(f"Fehler bei der Installation von python-magic: {output}")
            return False
        
        # Erneut testen
        with open('test_magic.py', 'w') as f:
            f.write(test_script)
        
        success, output = run_command("python test_magic.py")
        os.remove('test_magic.py')
        
        if 'SUCCESS' in output:
            log_message("libmagic-Test erfolgreich mit dem alternativen Paket.")
            return True
        else:
            log_message(f"libmagic-Test fehlgeschlagen mit allen Paketen: {output}")
            return False

def install_libmagic_macos():
    """Installiert libmagic für macOS"""
    log_message("Installation von libmagic und python-magic für macOS...")
    
    # Prüfen, ob Homebrew verfügbar ist
    success, _ = run_command("brew --version")
    if not success:
        log_message("Homebrew nicht gefunden. Versuche, es zu installieren...")
        install_command = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        success, output = run_command(install_command)
        if not success:
            log_message(f"Fehler bei der Installation von Homebrew: {output}")
            log_message("Bitte installieren Sie Homebrew manuell: https://brew.sh")
            return False
    
    # Installiere libmagic über Homebrew
    log_message("Installation von libmagic über Homebrew...")
    success, output = run_command("brew install libmagic")
    
    if not success:
        log_message(f"Fehler bei der Installation von libmagic: {output}")
        return False
    
    # Installiere python-magic über pip
    log_message("Installation von python-magic...")
    success, output = run_command("pip install python-magic")
    
    if not success:
        log_message(f"Fehler bei der Installation von python-magic: {output}")
        return False
    
    log_message("Installation von libmagic und python-magic erfolgreich abgeschlossen.")
    
    # Überprüfen, ob die Installation funktioniert
    test_script = """
import magic
try:
    magic.Magic()
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {str(e)}')
"""
    
    with open('test_magic.py', 'w') as f:
        f.write(test_script)
    
    success, output = run_command("python test_magic.py")
    os.remove('test_magic.py')
    
    if 'SUCCESS' in output:
        log_message("libmagic-Test erfolgreich: Die Bibliothek funktioniert korrekt.")
        return True
    else:
        log_message(f"libmagic-Test fehlgeschlagen: {output}")
        return False

def install_libmagic_linux():
    """Installiert libmagic für Linux"""
    log_message("Installation von libmagic und python-magic für Linux...")
    
    # Erkennen der Linux-Distribution
    if os.path.exists('/etc/debian_version'):
        # Debian/Ubuntu
        log_message("Debian/Ubuntu-basiertes System erkannt")
        install_cmd = "apt-get update && apt-get install -y libmagic1 python3-magic"
        
        # Wenn sudo verfügbar ist, sudo verwenden
        success, _ = run_command("which sudo")
        if success:
            install_cmd = "sudo " + install_cmd
    
    elif os.path.exists('/etc/fedora-release') or os.path.exists('/etc/redhat-release'):
        # Fedora/RHEL/CentOS
        log_message("Fedora/RHEL/CentOS-basiertes System erkannt")
        install_cmd = "dnf install -y file-libs python3-magic"
        
        # Wenn sudo verfügbar ist, sudo verwenden
        success, _ = run_command("which sudo")
        if success:
            install_cmd = "sudo " + install_cmd
    
    elif os.path.exists('/etc/arch-release'):
        # Arch Linux
        log_message("Arch Linux-basiertes System erkannt")
        install_cmd = "pacman -Sy --noconfirm file python-magic"
        
        # Wenn sudo verfügbar ist, sudo verwenden
        success, _ = run_command("which sudo")
        if success:
            install_cmd = "sudo " + install_cmd
    
    else:
        # Generische Linux-Distribution
        log_message("Nicht erkannte Linux-Distribution. Versuche generischen Ansatz...")
        log_message("Stellen Sie sicher, dass libmagic und python-magic installiert sind.")
        
        # Versuchen, python-magic über pip zu installieren
        success, output = run_command("pip install python-magic")
        
        if not success:
            log_message(f"Fehler bei der Installation von python-magic: {output}")
            return False
        
        log_message("Python-magic über pip installiert. Überprüfen, ob die Systemabhängigkeiten erfüllt sind...")
        
        # Test
        test_script = """
import magic
try:
    magic.Magic()
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {str(e)}')
"""
        
        with open('test_magic.py', 'w') as f:
            f.write(test_script)
        
        success, output = run_command("python test_magic.py")
        os.remove('test_magic.py')
        
        if 'SUCCESS' in output:
            log_message("libmagic-Test erfolgreich: Die Bibliothek funktioniert korrekt.")
            return True
        else:
            log_message(f"libmagic-Test fehlgeschlagen: {output}")
            log_message("Bitte installieren Sie libmagic manuell für Ihre Linux-Distribution.")
            return False
    
    # Führe den Installationsbefehl aus
    log_message(f"Führe aus: {install_cmd}")
    success, output = run_command(install_cmd)
    
    if not success:
        log_message(f"Fehler bei der Installation von libmagic: {output}")
        
        # Versuche, python-magic über pip zu installieren
        log_message("Versuche, python-magic über pip zu installieren...")
        success, output = run_command("pip install python-magic")
        
        if not success:
            log_message(f"Fehler bei der Installation von python-magic: {output}")
            return False
    
    log_message("Installation von libmagic und python-magic erfolgreich abgeschlossen.")
    
    # Überprüfen, ob die Installation funktioniert
    test_script = """
import magic
try:
    magic.Magic()
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {str(e)}')
"""
    
    with open('test_magic.py', 'w') as f:
        f.write(test_script)
    
    success, output = run_command("python test_magic.py")
    os.remove('test_magic.py')
    
    if 'SUCCESS' in output:
        log_message("libmagic-Test erfolgreich: Die Bibliothek funktioniert korrekt.")
        return True
    else:
        log_message(f"libmagic-Test fehlgeschlagen: {output}")
        return False

def install_dependencies():
    """Installiert alle Abhängigkeiten aus der security_requirements.txt-Datei"""
    log_message("Installation der Sicherheitsabhängigkeiten aus security_requirements.txt...")
    
    if os.path.exists('security_requirements.txt'):
        success, output = run_command("pip install -r security_requirements.txt")
        
        if not success:
            log_message(f"Fehler bei der Installation der Sicherheitsabhängigkeiten: {output}")
            return False
        
        log_message("Sicherheitsabhängigkeiten erfolgreich installiert.")
        return True
    else:
        log_message("Warnung: security_requirements.txt nicht gefunden. Überspringe diesen Schritt.")
        return True

def restore_security_utils():
    """Stellt die Originalfunktionalität in app.py wieder her"""
    app_py_path = 'app.py'
    
    if not os.path.exists(app_py_path):
        log_message(f"Fehler: {app_py_path} nicht gefunden")
        return False
    
    try:
        # Datei lesen
        with open(app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Überprüfen, ob temporäre Ersatzfunktionen vorhanden sind
        if "# Temporäre Ersatzfunktionen für security_utils" in content:
            log_message("Temporäre Ersatzfunktionen gefunden. Stelle security_utils-Import wieder her...")
            
            # Importzeile wiederherstellen
            if "#from security_utils import" in content:
                content = content.replace(
                    "#from security_utils import sanitize_html, validate_file_ext, validate_file_content, sanitize_input, sanitize_integer, sanitize_float, sanitize_filename",
                    "from security_utils import sanitize_html, validate_file_ext, validate_file_content, sanitize_input, sanitize_integer, sanitize_float, sanitize_filename"
                )
            
            # Temporäre Ersatzfunktionen entfernen
            start_marker = "# Temporäre Ersatzfunktionen für security_utils"
            end_marker = "# Ende der temporären Ersatzfunktionen"
            
            start_pos = content.find(start_marker)
            end_pos = content.find(end_marker)
            
            if start_pos != -1 and end_pos != -1:
                content = content[:start_pos] + content[end_pos + len(end_marker):]
            
            # Speichere die geänderte Datei
            with open(app_py_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            log_message("security_utils-Funktionalität in app.py erfolgreich wiederhergestellt.")
            return True
        else:
            log_message("Keine temporären Ersatzfunktionen in app.py gefunden. Nichts zu tun.")
            return True
    
    except Exception as e:
        log_message(f"Fehler beim Wiederherstellen der security_utils-Funktionalität: {str(e)}")
        return False

if __name__ == "__main__":
    log_message("Starte Installation und Konfiguration von libmagic...")
    
    # Betriebssystem erkennen
    os_type = detect_os()
    log_message(f"Betriebssystem erkannt: {os_type}")
    
    success = False
    
    # Je nach Betriebssystem installieren
    if os_type == 'windows':
        success = install_libmagic_windows()
    elif os_type == 'macos':
        success = install_libmagic_macos()
    elif os_type == 'linux':
        success = install_libmagic_linux()
    else:
        log_message("Nicht unterstütztes Betriebssystem. Bitte installieren Sie libmagic manuell.")
        success = False
    
    # Andere Abhängigkeiten installieren
    if success:
        install_dependencies()
        
        # security_utils-Funktionalität wiederherstellen
        restore_security_utils()
        
        log_message("Installation und Konfiguration von libmagic abgeschlossen.")
        log_message("Sie können die Anwendung jetzt mit python app.py starten.")
    else:
        log_message("Installation und Konfiguration von libmagic fehlgeschlagen.")
        log_message("Bitte prüfen Sie die Fehlermeldungen und versuchen Sie eine manuelle Installation.") 