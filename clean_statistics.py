from app import app, db
from models import PageVisit, DailyStats, GalleryView
from utils import get_friendly_page_name
import re
from datetime import datetime

def clean_statistics():
    with app.app_context():
        # 1. Entferne bestimmte API-Aufrufe und unerwünschte Pfade
        api_patterns = [
            '/favicon.ico',
            '/get_visit_id',
            '/get_api_key_token',
            '/track_image_view',
            '/update_visit_duration'
        ]
        
        total_removed = 0
        for pattern in api_patterns:
            api_visits = PageVisit.query.filter(PageVisit.page.like(f'%{pattern}%')).all()
            if api_visits:
                print(f"Entferne {len(api_visits)} Einträge für Pfad '{pattern}'...")
                for visit in api_visits:
                    db.session.delete(visit)
                total_removed += len(api_visits)
        
        if total_removed > 0:
            db.session.commit()
            print(f"Insgesamt {total_removed} API-/System-Einträge entfernt.")
        else:
            print("Keine API-/System-Einträge gefunden.")
            
        # 2. Aktualisiere alle bestehenden Einträge mit verbesserten benutzerfreundlichen Namen
        print("Aktualisiere benutzerfreundliche Namen für alle Seitenbesuche...")
        all_visits = PageVisit.query.all()
        updated_count = 0
        
        for visit in all_visits:
            # Verwende die aktualisierte get_friendly_page_name-Funktion
            new_friendly_name = get_friendly_page_name(visit.page)
            
            # Aktualisiere nur, wenn sich der Name geändert hat
            if new_friendly_name != visit.page_friendly_name:
                visit.page_friendly_name = new_friendly_name
                updated_count += 1
        
        if updated_count > 0:
            db.session.commit()
            print(f"{updated_count} Einträge mit neuen benutzerfreundlichen Namen aktualisiert.")
        else:
            print("Keine Einträge mussten aktualisiert werden.")

def reset_all_statistics():
    """Löscht ALLE Statistikdaten und setzt alles auf 0 zurück"""
    with app.app_context():
        try:
            # 1. Alle PageVisit-Einträge löschen
            visits_count = PageVisit.query.count()
            PageVisit.query.delete()
            print(f"{visits_count} Seitenbesuche gelöscht")
            
            # 2. Alle GalleryView-Einträge löschen
            gallery_views_count = GalleryView.query.count()
            GalleryView.query.delete()
            print(f"{gallery_views_count} Galerie-Ansichten gelöscht")
            
            # 3. Alle DailyStats-Einträge löschen
            stats_count = DailyStats.query.count()
            DailyStats.query.delete()
            print(f"{stats_count} Tagesstatistiken gelöscht")
            
            # 4. Einen leeren DailyStats-Eintrag für heute erstellen
            today = datetime.now().date()
            empty_stats = DailyStats(
                date=today,
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
            db.session.add(empty_stats)
            
            # 5. Änderungen speichern
            db.session.commit()
            print(f"Statistiken vollständig zurückgesetzt. Neue leere Tagesstatistik für {today} erstellt.")
            
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Fehler beim Zurücksetzen der Statistiken: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
if __name__ == "__main__":
    # Frage den Benutzer, ob er die Statistiken bereinigen oder zurücksetzen möchte
    print("Was möchten Sie tun?")
    print("1. Statistiken bereinigen (API-Aufrufe entfernen, Namen aktualisieren)")
    print("2. Statistiken VOLLSTÄNDIG zurücksetzen (ALLE Daten werden gelöscht!)")
    
    choice = input("Bitte geben Sie 1 oder 2 ein: ")
    
    if choice == '1':
        clean_statistics()
        print("Statistiken-Bereinigung abgeschlossen.")
    elif choice == '2':
        confirm = input("WARNUNG: Alle Statistikdaten werden unwiderruflich gelöscht! Fortfahren? (j/n): ")
        if confirm.lower() == 'j':
            if reset_all_statistics():
                print("Statistiken wurden vollständig zurückgesetzt.")
            else:
                print("Fehler beim Zurücksetzen der Statistiken.")
        else:
            print("Vorgang abgebrochen.")
    else:
        print("Ungültige Eingabe. Vorgang abgebrochen.") 