import re
from flask import request, session, current_app
from models import db, PageVisit, GalleryView, DailyStats, GalleryImage
from datetime import datetime, timedelta
import logging
import json

# Logger konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('utils')

# Hilfsfunktion zur Ermittlung eines benutzerfreundlichen Seitennamens
def get_friendly_page_name(page):
    # Überprüfe, ob page None ist
    if page is None:
        return "Unbekannte Seite"
        
    # Spezielle Behandlung für API und System-Aufrufe - nicht in Statistiken anzeigen
    api_system_paths = [
        '/favicon.ico',
        '/get_visit_id',
        '/get_api_key_token',
        '/track_image_view',
        '/update_visit_duration',
        '/api/',
        '/static/'
    ]
    
    # Wenn der Pfad ein API- oder System-Pfad ist, einen aussagekräftigen Namen zurückgeben
    for path in api_system_paths:
        if page.startswith(path):
            # Statt None zurückzugeben, geben wir einen aussagekräftigen Namen zurück
            return "System: " + page
        
    page_names = {
        "/": "Startseite",
        "index": "Startseite",
        "/admin/statistiken": "Admin: Statistiken",
        "/admin": "Admin: Dashboard",
        "/admin/galerie": "Admin: Galerie",
        "/admin/speisekarte": "Admin: Speisekarte",
        "/admin/neuigkeiten": "Admin: Neuigkeiten",
        "/admin/oeffnungszeiten": "Admin: Öffnungszeiten",
        "/admin-panel/statistics": "Admin: Statistiken",
        "/admin-panel": "Admin: Dashboard",
        "/admin-panel/gallery": "Admin: Galerie",
        "/admin-panel/menu": "Admin: Speisekarte",
        "/admin-panel/news": "Admin: Neuigkeiten",
        "/admin-panel/opening-hours": "Admin: Öffnungszeiten",
        "/speisekarte": "Speisekarte",
        "/galerie": "Galerie",
        "/update_visit_duration": "Besuchsdauer-Tracking",
        "/salzgeschichte": "Salzgeschichte",
        "/familiengeschichte": "Familiengeschichte",
        "/erfahrungsgeschichte": "Erlebnisgeschichte",
        "/salz-geschichte": "Salzgeschichte",
        "/familien-geschichte": "Familiengeschichte",
        "/erfahrungs-geschichte": "Erfahrungsgeschichte",
        "/salt-story": "Salzgeschichte",
        "/salt_story": "Salzgeschichte",
        "/family-story": "Familiengeschichte",
        "/family_story": "Familiengeschichte",
        "/experience-story": "Erlebnisgeschichte",
        "/experience_story": "Erlebnisgeschichte",
        "/impressum": "Impressum",
        "/datenschutz": "Datenschutz",
        "/kontakt": "Kontakt",
        "/reservierung": "Reservierung",
        "/login": "Login-Seite",
        "/logout": "Logout"
    }
    
    # Exakte Übereinstimmung prüfen
    if page in page_names:
        return page_names[page]
    
    # Teilweise Übereinstimmung prüfen
    for key, value in page_names.items():
        if key in page and key != "/":  # Vermeide Übereinstimmung mit "/" für alle Pfade
            return value
    
    # Für Galerie-Bilder
    if page.startswith('/galerie/bild/'):
        return "Galerie: Einzelbild"
    
    # Für Speisekarte-Kategorien
    if page.startswith('/speisekarte/kategorie/'):
        category = page.split('/')[-1]
        return f"Speisekarte: {category.capitalize()}"
    
    # Wenn kein passender Name gefunden wurde, gib einen generischen Namen zurück
    return f"Seite: {page}"

def track_page_visit(page):
    """Trackt einen Seitenaufruf in der Datenbank und aktualisiert die Statistiken."""
    try:
        # Überprüfen, ob page None ist - wenn ja, früh abbrechen
        if page is None:
            print("[TRACK_VISIT] Abgebrochen: page ist None")
            return
        
        # Doppelte Besuche innerhalb eines kurzen Zeitraums vermeiden (z.B. durch Neuladen)
        # Prüfe, ob es bereits einen Besuch von derselben IP zur selben Seite in den letzten 5 Sekunden gibt
        
        # IP-Adresse des Clients ermitteln (mit Proxy-Unterstützung)
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        else:
            ip_address = request.remote_addr
        
        now = datetime.now()
        five_seconds_ago = now - timedelta(seconds=5)
        
        # Suche nach einem kürzlichen Besuch mit derselben IP und Seite
        recent_visit = PageVisit.query.filter(
            PageVisit.ip_address == ip_address,
            PageVisit.page == page,
            PageVisit.timestamp > five_seconds_ago
        ).first()
        
        # Wenn ein kürzlicher Besuch gefunden wurde, nicht erneut zählen
        if recent_visit:
            print(f"[TRACK_VISIT] Doppelter Besuch ignoriert: {ip_address} auf {page}")
            return
        
        # Statistiken für den heutigen Tag abrufen oder erstellen
        today = datetime.now().date()
        daily_stats = DailyStats.query.filter_by(date=today).first()
        if not daily_stats:
            daily_stats = DailyStats(date=today, total_visits=0, unique_visitors=0)
            db.session.add(daily_stats)
        
        # Gesamtzahl der Besuche erhöhen
        daily_stats.total_visits += 1
        
        # Überprüfen, ob diese IP heute bereits gezählt wurde
        # Suche nach Besuchen von dieser IP heute
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        existing_ip_today = PageVisit.query.filter(
            PageVisit.ip_address == ip_address,
            PageVisit.timestamp >= today_start,
            PageVisit.timestamp < now  # Nur bestehende Besuche prüfen
        ).first()
        
        if not existing_ip_today:
            print(f"[TRACK_VISIT] Neue IP heute: {ip_address}. Erhöhe eindeutige Besucher.")
            daily_stats.unique_visitors += 1
        
        # Freundlichen Seitennamen ermitteln
        friendly_name = get_friendly_page_name(page)
        
        # Seitenaufruf in PageVisit speichern
        user_agent = request.headers.get('User-Agent', '')
        referer = request.headers.get('Referer', '')
        
        visit = PageVisit(
            page=page,
            page_friendly_name=friendly_name,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.now()
        )
        db.session.add(visit)
        
        # Änderungen in der Datenbank speichern
        db.session.commit()
        print(f"[TRACK_VISIT] Erfolg: Besuch für {page} ({friendly_name}) von {ip_address} wurde gespeichert")
        
    except Exception as e:
        db.session.rollback()
        print(f"[TRACK_VISIT] Fehler beim Tracken des Besuchs: {str(e)}")
        import traceback
        traceback.print_exc()

def update_visit_duration(visit_id, duration, screen_width=None, screen_height=None):
    """Aktualisiert die Verweildauer und Bildschirmgröße eines Besuchs"""
    try:
        print(f"DEBUG: Verweildauer-Update für Besuch {visit_id} mit Dauer {duration}s gestartet")
        visit = PageVisit.query.get(visit_id)
        
        if not visit:
            print(f"DEBUG: Besuch mit ID {visit_id} nicht gefunden!")
            return False
            
        print(f"DEBUG: Besuch gefunden - aktuelle Dauer: {visit.duration}s, Analytics-Zustimmung: {visit.analytics_consent}")
        
        # Dauer aktualisieren, unabhängig von der Analytics-Zustimmung, um die Datenbank korrekt zu halten
        # Nur aktualisieren, wenn sich die Dauer erhöht hat
        if visit.duration is None or duration > visit.duration:
            old_duration = visit.duration
            visit.duration = duration
            print(f"DEBUG: Besuchsdauer aktualisiert von {old_duration}s auf {duration}s")
            
        if screen_width and screen_height:
            visit.screen_width = screen_width
            visit.screen_height = screen_height
            print(f"DEBUG: Bildschirmgröße aktualisiert: {screen_width}x{screen_height}")
        
        # Aktualisiere die durchschnittliche Verweildauer in der Tagesstatistik
        today = datetime.now().date()
        stats = DailyStats.query.filter_by(date=today).first()
        
        if not stats:
            print(f"DEBUG: Keine Tagesstatistik für heute ({today}) gefunden, erstelle neu")
            stats = DailyStats(
                date=today,
                total_visits=0,
                unique_visitors=0,
                gallery_views=0,
                chrome_users=0,
                firefox_users=0,
                safari_users=0,
                edge_users=0,
                other_browsers=0,
                windows_users=0,
                mac_users=0,
                linux_users=0,
                ios_users=0,
                android_users=0,
                other_os=0,
                mobile_users=0,
                desktop_users=0,
                consent_count=0
            )
            db.session.add(stats)
            db.session.flush()
            
        # Debug-Informationen für die Verweildauer-Berechnung
        print(f"DEBUG: Berechne durchschnittliche Verweildauer für {today}")
        
        # Berechne den neuen Durchschnitt - alle Besuche mit Dauer berücksichtigen
        # Nur Seiten berücksichtigen, die nicht mit /admin oder /admin-panel beginnen
        visits_with_duration = PageVisit.query.filter(
            PageVisit.timestamp >= datetime.combine(today, datetime.min.time()),
            PageVisit.timestamp <= datetime.combine(today, datetime.max.time()),
            PageVisit.duration.isnot(None),
            ~PageVisit.page.startswith('/admin'),
            ~PageVisit.page.startswith('/admin-panel'),
            ~PageVisit.page.startswith('/static'),
            ~PageVisit.page.startswith('/update_visit_duration'),
            ~PageVisit.page.startswith('/api')
        ).all()
        
        if visits_with_duration:
            print(f"DEBUG: {len(visits_with_duration)} Besuche mit Verweildauer gefunden")
            
            # Gruppiere Besuche nach IP-Adresse, um je Benutzer nur einen Besuch pro Tag zu zählen
            ip_duration_map = {}
            for v in visits_with_duration:
                # Nehme für jede IP-Adresse die längste Verweildauer
                if v.ip_address not in ip_duration_map or v.duration > ip_duration_map[v.ip_address]:
                    ip_duration_map[v.ip_address] = v.duration
            
            # Berechne den Durchschnitt basierend auf der längsten Verweildauer je IP-Adresse
            if ip_duration_map:
                total_duration = sum(ip_duration_map.values())
                unique_ips = len(ip_duration_map)
                avg_duration = total_duration / unique_ips
                
                print(f"DEBUG: Durchschnittliche Verweildauer berechnet: {avg_duration:.2f}s "
                      f"basierend auf {unique_ips} eindeutigen Besuchern")
                
                stats.avg_duration = avg_duration
                db.session.add(stats)
                db.session.commit()
                return True
            else:
                print("DEBUG: Keine eindeutigen IPs mit Verweildauer gefunden.")
                return False
        else:
            print("DEBUG: Keine Besuche mit Verweildauer für heute gefunden.")
            return False
    except Exception as e:
        db.session.rollback()
        print(f"Fehler beim Aktualisieren der Verweildauer: {e}")
        import traceback
        traceback.print_exc()
        return False

def track_gallery_view(image_id):
    try:
        # Prüfe, ob wir im Kontext einer Anfrage sind (für Tests)
        if not has_request_context():
            print("Kein Request-Kontext, überspringe Tracking...")
            return None

        # Ermittle die echte IP-Adresse (auch hinter Proxies)
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_address and ',' in ip_address:
            # Wenn mehrere IPs in X-Forwarded-For, nehme die erste (Client-IP)
            ip_address = ip_address.split(',')[0].strip()
            
        # Falls die IP-Adresse immer noch leer ist, verwende localhost
        if not ip_address:
            ip_address = '127.0.0.1'
            
        now = datetime.now()
        
        # Prüfen, ob das Bild existiert
        image = GalleryImage.query.get(image_id)
        if not image:
            print(f"Bild mit ID {image_id} nicht gefunden.")
            return None
            
        # Debug-Info
        print(f"Tracking Bildaufruf: ID={image_id}, IP={ip_address}")
        
        # Prüfe, ob der Benutzer das Bild heute bereits angesehen hat
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        previous_view = GalleryView.query.filter(
            GalleryView.image_id == image_id,
            GalleryView.ip_address == ip_address,
            GalleryView.timestamp >= today_start
        ).first()
        
        # Wenn bereits angesehen, aktualisiere nur den Zeitstempel und zähle nicht erneut
        if previous_view:
            print(f"Benutzer {ip_address} hat Bild {image_id} heute bereits angesehen.")
            previous_view.timestamp = now
            db.session.commit()
            return previous_view.id
            
        # Neuen Aufruf erstellen
        view = GalleryView(
            image_id=image_id,
            ip_address=ip_address,
            timestamp=now
        )
        db.session.add(view)
        
        # Galerieaufrufe in der Tagesstatistik erhöhen
        stats = DailyStats.query.filter_by(date=now.date()).first()
        
        if not stats:
            stats = DailyStats(
                date=now.date(),
                total_visits=0,
                unique_visitors=0,
                gallery_views=0,
                consent_count=0,
                chrome_users=0,
                firefox_users=0,
                safari_users=0,
                edge_users=0,
                other_browsers=0,
                windows_users=0,
                mac_users=0,
                linux_users=0,
                ios_users=0,
                android_users=0,
                other_os=0,
                mobile_users=0,
                desktop_users=0
            )
            db.session.add(stats)
            
        stats.gallery_views += 1
        db.session.commit()
        
        return view.id
    except Exception as e:
        db.session.rollback()
        print(f"Fehler beim Tracking des Galerieaufrufs: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_statistics():
    """
    Holt Statistiken der letzten 30 Tage für die Statistikseite.
    Stellt sicher, dass ein Eintrag für den aktuellen Tag existiert.
    
    Returns:
        dict: Dictionary mit gesammelten Statistiken
    """
    from models import db, DailyStats, PageVisit, GalleryView, GalleryImage
    from datetime import datetime, timedelta
    import traceback

    # Stelle sicher, dass ein Eintrag für heute existiert
    today = datetime.now().date()
    today_stats = DailyStats.query.filter_by(date=today).first()
    if not today_stats:
        # Erstelle Eintrag für heute, falls nicht vorhanden
        today_stats = DailyStats(date=today)
        db.session.add(today_stats)
        db.session.commit()

    # Berechne Datum von vor 30 Tagen
    thirty_days_ago = today - timedelta(days=30)
    
    try:
        # Hole Statistik-Einträge der letzten 30 Tage
        daily_stats = DailyStats.query.filter(
            DailyStats.date >= thirty_days_ago,
            DailyStats.date <= today
        ).order_by(DailyStats.date.desc()).all()
        
        # Initialisiere Statistiken
        result = {
            'thirty_days_ago': thirty_days_ago,
            'daily_stats': daily_stats,
            'total_visits': 0,
            'unique_visitors': 0,
            'total_gallery_views': 0,
            'avg_duration': 0,
            'browser_stats': {
                'chrome': 0, 
                'firefox': 0, 
                'safari': 0, 
                'edge': 0, 
                'other': 0
            },
            'os_stats': {
                'windows': 0, 
                'mac': 0, 
                'linux': 0, 
                'ios': 0, 
                'android': 0, 
                'other': 0
            },
            'device_stats': {
                'desktop': 0, 
                'mobile': 0
            },
            'cookie_consent': {
                'analytics': 0, 
                'only_necessary': 0
            },
            'page_visits': [],
            'gallery_views': [],
            'daily_unique_ips': {}
        }
        
        # Summiere die Statistiken der letzten 30 Tage
        visit_count_with_duration = 0
        total_duration = 0
        
        for stat in daily_stats:
            result['total_visits'] += stat.total_visits
            result['unique_visitors'] += stat.unique_visitors
            result['total_gallery_views'] += stat.gallery_views
            
            # Browser-Statistiken
            result['browser_stats']['chrome'] += stat.chrome_users
            result['browser_stats']['firefox'] += stat.firefox_users
            result['browser_stats']['safari'] += stat.safari_users
            result['browser_stats']['edge'] += stat.edge_users
            result['browser_stats']['other'] += stat.other_browsers
            
            # Betriebssystem-Statistiken
            result['os_stats']['windows'] += stat.windows_users
            result['os_stats']['mac'] += stat.mac_users
            result['os_stats']['linux'] += stat.linux_users
            result['os_stats']['ios'] += stat.ios_users
            result['os_stats']['android'] += stat.android_users
            result['os_stats']['other'] += stat.other_os
            
            # Gerätetyp-Statistiken
            result['device_stats']['desktop'] += stat.desktop_users
            result['device_stats']['mobile'] += stat.mobile_users
            
            # Cookie-Zustimmung
            result['cookie_consent']['analytics'] += stat.consent_count
            result['cookie_consent']['only_necessary'] += max(0, stat.unique_visitors - stat.consent_count)
            
            # Für die Berechnung der durchschnittlichen Verweildauer
            if stat.avg_duration and stat.avg_duration > 0:
                visit_count_with_duration += 1
                total_duration += stat.avg_duration
        
        # Berechne durchschnittliche Verweildauer über alle Tage
        if visit_count_with_duration > 0:
            result['avg_duration'] = total_duration / visit_count_with_duration
            
        # Hole Seitenaufrufe nach Seite (nach freundlichem Namen gruppiert)
        page_visits_query = db.session.query(
            PageVisit.page, 
            db.func.count(PageVisit.id).label('visit_count')
        ).filter(
            PageVisit.timestamp >= datetime.combine(thirty_days_ago, datetime.min.time()),
            ~PageVisit.page.like('/admin%'),  # Keine Admin-Seiten
            ~PageVisit.page.like('/api/%')    # Keine API-Aufrufe
        ).group_by(PageVisit.page).order_by(db.desc('visit_count')).all()
        
        for path, count in page_visits_query:
            friendly_name = get_friendly_page_name(path)
            if friendly_name:  # Filtere alle, die None zurückgeben
                result['page_visits'].append((friendly_name, count))
                
        # Hole Galerie-Aufrufe nach Bild
        gallery_views_query = db.session.query(
            GalleryImage.title, 
            db.func.count(GalleryView.id).label('view_count')
        ).join(
            GalleryView, GalleryView.image_id == GalleryImage.id
        ).filter(
            GalleryView.timestamp >= datetime.combine(thirty_days_ago, datetime.min.time())
        ).group_by(GalleryImage.title).order_by(db.desc('view_count')).all()
        
        result['gallery_views'] = gallery_views_query
        
        # Hole eindeutige IP-Adressen pro Tag
        for stat in daily_stats:
            # Hole IP-Adressen und deren Anzahl an Besuchen für diesen Tag
            day_start = datetime.combine(stat.date, datetime.min.time())
            day_end = datetime.combine(stat.date, datetime.max.time())
            
            ip_counts = db.session.query(
                PageVisit.ip_address, 
                db.func.count(PageVisit.id).label('visit_count')
            ).filter(
                PageVisit.timestamp >= day_start,
                PageVisit.timestamp <= day_end
            ).group_by(PageVisit.ip_address).order_by(db.desc('visit_count')).all()
            
            result['daily_unique_ips'][stat.date] = ip_counts
            
        return result
    
    except Exception as e:
        print(f"Fehler beim Abrufen der Statistiken: {e}")
        print(traceback.format_exc())
        return {
            'thirty_days_ago': thirty_days_ago,
            'daily_stats': [],
            'total_visits': 0,
            'unique_visitors': 0,
            'total_gallery_views': 0,
            'avg_duration': 0,
            'browser_stats': {'chrome': 0, 'firefox': 0, 'safari': 0, 'edge': 0, 'other': 0},
            'os_stats': {'windows': 0, 'mac': 0, 'linux': 0, 'ios': 0, 'android': 0, 'other': 0},
            'device_stats': {'desktop': 0, 'mobile': 0},
            'cookie_consent': {'analytics': 0, 'only_necessary': 0},
            'page_visits': [],
            'gallery_views': [],
            'daily_unique_ips': {}
        }

def detect_browser(user_agent_string):
    """Erkennt den Browser-Typ aus dem User-Agent-String."""
    if not user_agent_string:
        return "Unbekannt"
    
    user_agent_lower = user_agent_string.lower()
    
    if "chrome" in user_agent_lower and "edge" not in user_agent_lower:
        return "Chrome"
    elif "firefox" in user_agent_lower:
        return "Firefox"
    elif "safari" in user_agent_lower and "chrome" not in user_agent_lower:
        return "Safari"
    elif "edge" in user_agent_lower:
        return "Edge"
    else:
        return "Andere"

def detect_os(user_agent_string):
    """Erkennt das Betriebssystem aus dem User-Agent-String."""
    if not user_agent_string:
        return "Unbekannt"
    
    user_agent_lower = user_agent_string.lower()
    
    if "windows" in user_agent_lower:
        return "Windows"
    elif "macintosh" in user_agent_lower or "mac os" in user_agent_lower:
        return "Mac"
    elif "linux" in user_agent_lower:
        return "Linux"
    elif "iphone" in user_agent_lower or "ipad" in user_agent_lower:
        return "iOS"
    elif "android" in user_agent_lower:
        return "Android"
    else:
        return "Andere"

def detect_mobile(user_agent_string):
    """Erkennt, ob der Benutzer ein mobiles Gerät verwendet."""
    if not user_agent_string:
        return False
    
    user_agent_lower = user_agent_string.lower()
    
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'windows phone']
    return any(keyword in user_agent_lower for keyword in mobile_keywords)
