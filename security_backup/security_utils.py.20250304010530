"""
Sicherheits-Hilfsfunktionen für die Restaurant-Website.
Dieses Modul enthält Funktionen zur Verbesserung der allgemeinen Sicherheit,
einschließlich Schutz vor XSS, CSRF und Dateisystem-Angriffen.
"""

import os
import re
import magic
from werkzeug.utils import secure_filename
import bleach

# Liste der erlaubten HTML-Tags für die Beschreibung
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'span', 'div', 'b', 'i'
]

# Liste der erlaubten HTML-Attribute
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'style']
}

# Liste der erlaubten CSS-Eigenschaften 
ALLOWED_STYLES = [
    'color', 'font-weight', 'text-align', 'text-decoration',
    'font-style', 'font-size', 'line-height', 'margin', 'padding'
]

# Erlaubte Dateiendungen für Uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Erlaubte MIME-Typen für hochgeladene Dateien
ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp'
}

def is_safe_path(base_dir, path):
    """
    Überprüft, ob ein Pfad sicher ist und nicht außerhalb des Basisverzeichnisses liegt.
    
    Args:
        base_dir: Das Basisverzeichnis, in dem der Pfad liegen sollte
        path: Der zu überprüfende Pfad
        
    Returns:
        bool: True, wenn der Pfad sicher ist, sonst False
    """
    real_base = os.path.realpath(base_dir)
    real_path = os.path.realpath(os.path.join(base_dir, path))
    return real_path.startswith(real_base)

def sanitize_html(content):
    """
    Bereinigt HTML-Inhalte, um XSS-Angriffe zu verhindern.
    
    Args:
        content: Der zu bereinigende HTML-Inhalt
        
    Returns:
        str: Der bereinigte HTML-Inhalt
    """
    if content is None:
        return ""
    
    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        styles=ALLOWED_STYLES,
        strip=True
    )

def validate_file_ext(filename):
    """
    Überprüft, ob der Dateiname eine erlaubte Erweiterung hat.
    
    Args:
        filename: Der zu überprüfende Dateiname
        
    Returns:
        bool: True, wenn die Dateiendung erlaubt ist, sonst False
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_content(file_path):
    """
    Validiert den Inhalt einer Datei durch Überprüfung des MIME-Typs.
    
    Args:
        file_path: Der Pfad zur zu überprüfenden Datei
        
    Returns:
        bool: True, wenn der MIME-Typ erlaubt ist, sonst False
    """
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        return file_type in ALLOWED_MIME_TYPES
    except Exception:
        return False

def sanitize_filename(filename):
    """
    Erzeugt einen sicheren Dateinamen basierend auf Werkzeug's secure_filename.
    Entfernt alle potenziell gefährlichen Zeichen.
    
    Args:
        filename: Der ursprüngliche Dateiname
        
    Returns:
        str: Der bereinigte Dateiname
    """
    return secure_filename(filename)

def sanitize_input(input_str):
    """
    Bereinigt einen Eingabestring für die sichere Verwendung in HTML.
    
    Args:
        input_str: Der zu bereinigende String
        
    Returns:
        str: Der bereinigte String
    """
    if input_str is None:
        return ""
    
    # Entfernt potenziell gefährliche Zeichen
    sanitized = re.sub(r'[^\w\s.,!?-]', '', input_str)
    return sanitized.strip()

def sanitize_integer(value, default=0, min_value=None, max_value=None):
    """
    Stellt sicher, dass ein Wert ein gültiger Integer ist und innerhalb erlaubter Grenzen liegt.
    
    Args:
        value: Der zu überprüfende Wert
        default: Der Standardwert bei ungültiger Eingabe
        min_value: Der minimale erlaubte Wert (optional)
        max_value: Der maximale erlaubte Wert (optional)
        
    Returns:
        int: Der validierte Integer-Wert
    """
    try:
        result = int(value)
        
        if min_value is not None and result < min_value:
            return min_value
            
        if max_value is not None and result > max_value:
            return max_value
            
        return result
    except (ValueError, TypeError):
        return default

def sanitize_float(value, default=0.0, min_value=None, max_value=None):
    """
    Stellt sicher, dass ein Wert ein gültiger Float ist und innerhalb erlaubter Grenzen liegt.
    
    Args:
        value: Der zu überprüfende Wert
        default: Der Standardwert bei ungültiger Eingabe
        min_value: Der minimale erlaubte Wert (optional)
        max_value: Der maximale erlaubte Wert (optional)
        
    Returns:
        float: Der validierte Float-Wert
    """
    try:
        result = float(value)
        
        if min_value is not None and result < min_value:
            return min_value
            
        if max_value is not None and result > max_value:
            return max_value
            
        return result
    except (ValueError, TypeError):
        return default 