from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from flask_wtf.csrf import validate_csrf
from models import db, OpeningHours, MenuItem, MenuCategory, GalleryImage, PageVisit, GalleryView, DailyStats, GalleryCategory, User
from datetime import datetime, time, timedelta
from forms import OpeningHoursForm
from sqlalchemy import func, extract, cast, Date
from flask_wtf import FlaskForm
import os
from werkzeug.utils import secure_filename
from flask import current_app
import calendar
import json
from collections import defaultdict
from utils import get_friendly_page_name
from flask_paginate import Pagination

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
def index():
    # Manuelle Authentifizierungsprüfung
    if not current_user.is_authenticated:
        # Statt 404-Fehler zurückzugeben, leiten wir zu /admin um
        return redirect('/admin')
    return render_template('admin/index.html')

@admin.route('/oeffnungszeiten')
@login_required
def opening_hours():
    hours = OpeningHours.query.order_by(
        db.case(
            {'Montag': 1, 'Dienstag': 2, 'Mittwoch': 3, 
             'Donnerstag': 4, 'Freitag': 5, 'Samstag': 6, 'Sonntag': 7},
            value=OpeningHours.day
        )
    ).all()
    
    # Automatische Überprüfung und Zurücksetzung von abgelaufenen Urlaubstagen
    for hour in hours:
        hour.check_vacation_expired()
    db.session.commit()
    
    form = OpeningHoursForm()
    return render_template('admin/opening_hours.html', hours=hours, form=form)

@admin.route('/oeffnungszeiten/hinzufuegen', methods=['POST'])
@login_required
def add_opening_hours():
    try:
        form = OpeningHoursForm()
        if not form.validate_on_submit():
            return jsonify({'success': False, 'message': 'CSRF-Token ungültig'}), 400

        day = request.form.get('day')
        if not day:
            return jsonify({'success': False, 'message': 'Tag muss angegeben werden.'})
            
        if OpeningHours.query.filter_by(day=day).first():
            return jsonify({'success': False, 'message': f'Öffnungszeiten für {day} existieren bereits.'})
        
        hours = OpeningHours(day=day)
        
        vacation_active = request.form.get('vacation_active') == 'true'
        closed = request.form.get('closed') == 'true'
        
        if vacation_active and closed:
            return jsonify({'success': False, 'message': 'Ein Tag kann nicht gleichzeitig Urlaub und Ruhetag sein.'})
        
        if vacation_active:
            vacation_start = request.form.get('vacation_start')
            vacation_end = request.form.get('vacation_end')
            
            if not vacation_start or not vacation_end:
                return jsonify({'success': False, 'message': 'Bitte geben Sie Start- und Enddatum für den Urlaub an.'})
                
            try:
                hours.vacation_start = datetime.strptime(vacation_start, '%Y-%m-%d').date()
                hours.vacation_end = datetime.strptime(vacation_end, '%Y-%m-%d').date()
                hours.vacation_active = True
                
                # Validiere Urlaubsdaten
                hours.validate_vacation()
            except ValueError as e:
                return jsonify({'success': False, 'message': str(e)})
                
        elif closed:
            hours.closed = True
        else:
            open_time_1 = request.form.get('open_time_1')
            close_time_1 = request.form.get('close_time_1')
            
            if not open_time_1 or not close_time_1:
                return jsonify({'success': False, 'message': 'Bitte geben Sie mindestens die erste Öffnungszeit an.'})
            
            hours.open_time_1 = open_time_1
            hours.close_time_1 = close_time_1
            
            open_time_2 = request.form.get('open_time_2')
            close_time_2 = request.form.get('close_time_2')
            
            if open_time_2 or close_time_2:
                if not open_time_2 or not close_time_2:
                    return jsonify({'success': False, 'message': 'Bitte geben Sie beide Zeiten für die zweite Öffnungszeit an.'})
                hours.open_time_2 = open_time_2
                hours.close_time_2 = close_time_2
            
            try:
                hours.validate_times()
            except ValueError as e:
                return jsonify({'success': False, 'message': str(e)})

        db.session.add(hours)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Öffnungszeiten für {day} wurden erfolgreich hinzugefügt.',
            'hours': hours.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@admin.route('/oeffnungszeiten/<int:id>', methods=['GET'])
@login_required
def get_opening_hours(id):
    try:
        hours = OpeningHours.query.get_or_404(id)
        return jsonify({
            'success': True,
            'hours': hours.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@admin.route('/oeffnungszeiten/bearbeiten/<int:id>', methods=['POST'])
@login_required
def edit_opening_hours(id):
    try:
        form = OpeningHoursForm()
        if not form.validate_on_submit():
            return jsonify({'success': False, 'message': 'CSRF-Token ungültig'}), 400

        hours = OpeningHours.query.get_or_404(id)
        
        # Validiere den Tag
        day = request.form.get('day')
        if not day:
            return jsonify({'success': False, 'message': 'Tag muss angegeben werden.'})
            
        existing_hours = OpeningHours.query.filter_by(day=day).first()
        if existing_hours and existing_hours.id != id:
            return jsonify({'success': False, 'message': f'Öffnungszeiten für {day} existieren bereits.'})
        
        hours.day = day
        
        # Validiere Urlaub und geschlossen Status
        vacation_active = request.form.get('vacation_active') == 'true'
        closed = request.form.get('closed') == 'true'
        
        if vacation_active and closed:
            return jsonify({'success': False, 'message': 'Ein Tag kann nicht gleichzeitig Urlaub und Ruhetag sein.'})
        
        # Setze alle Werte zurück
        hours.vacation_active = False
        hours.vacation_start = None
        hours.vacation_end = None
        hours.closed = False
        hours.open_time_1 = None
        hours.close_time_1 = None
        hours.open_time_2 = None
        hours.close_time_2 = None
        
        # Verarbeite die unterschiedlichen Modi
        if vacation_active:
            # Urlaubsmodus
            vacation_start = request.form.get('vacation_start')
            vacation_end = request.form.get('vacation_end')
            
            if not vacation_start or not vacation_end:
                return jsonify({'success': False, 'message': 'Bitte geben Sie Start- und Enddatum für den Urlaub an.'})
                
            try:
                hours.vacation_start = datetime.strptime(vacation_start, '%Y-%m-%d').date()
                hours.vacation_end = datetime.strptime(vacation_end, '%Y-%m-%d').date()
                hours.vacation_active = True
                
                # Validiere Urlaubsdaten
                hours.validate_vacation()
            except ValueError as e:
                return jsonify({'success': False, 'message': str(e)})
                
        elif closed:
            # Ruhetag
            hours.closed = True
        else:
            # Normaler Öffnungstag
            open_time_1 = request.form.get('open_time_1')
            close_time_1 = request.form.get('close_time_1')
            
            if not open_time_1 or not close_time_1:
                return jsonify({'success': False, 'message': 'Bitte geben Sie mindestens die erste Öffnungszeit an.'})
            
            hours.open_time_1 = open_time_1
            hours.close_time_1 = close_time_1
            
            open_time_2 = request.form.get('open_time_2')
            close_time_2 = request.form.get('close_time_2')
            
            if open_time_2 or close_time_2:
                if not open_time_2 or not close_time_2:
                    return jsonify({'success': False, 'message': 'Bitte geben Sie beide Zeiten für die zweite Öffnungszeit an.'})
                hours.open_time_2 = open_time_2
                hours.close_time_2 = close_time_2
            
            try:
                hours.validate_times()
            except ValueError as e:
                return jsonify({'success': False, 'message': str(e)})

        # Änderungen speichern
        db.session.commit()
        
        # Erfolgreiche Antwort senden
        response_data = {
            'success': True,
            'message': f'Öffnungszeiten für {day} wurden aktualisiert.',
            'hours': hours.to_dict()
        }
        
        # Debug-Ausgabe
        print(f"Antwortdaten: {response_data}")
        
        return jsonify(response_data)
        
    except Exception as e:
        db.session.rollback()
        print(f"Fehler beim Bearbeiten der Öffnungszeiten: {str(e)}")
        return jsonify({'success': False, 'message': f'Ein Fehler ist aufgetreten: {str(e)}'}), 500

@admin.route('/oeffnungszeiten/loeschen/<int:id>', methods=['POST'])
@login_required
def delete_opening_hours(id):
    try:
        hours = OpeningHours.query.get_or_404(id)
        day = hours.day
        db.session.delete(hours)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Öffnungszeiten für {day} wurden gelöscht.',
            'id': id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@admin.route('/speisekarte')
@login_required
def menu():
    categories = MenuCategory.query.order_by(MenuCategory.order).all()
    menu_items = MenuItem.query.order_by(MenuItem.category_id, MenuItem.order).all()
    form = FlaskForm()  # Create a form instance for CSRF token
    return render_template('admin/menu.html', 
                         categories=categories,
                         menu_items=menu_items,
                         form=form)

@admin.route('/menu')
@login_required
def menu_redirect():
    return redirect(url_for('admin.menu'))

@admin.route('/galerie')
@login_required
def gallery():
    categories = GalleryCategory.query.order_by(GalleryCategory.order).all()
    images = GalleryImage.query.order_by(GalleryImage.category_id, GalleryImage.order).all()
    return render_template('admin/gallery.html', categories=categories, images=images)

@admin.route('/gallery')
@login_required
def gallery_redirect():
    return redirect(url_for('admin.gallery'))

@admin.route('/gallery/add_category', methods=['POST'])
@login_required
def add_gallery_category():
    name = request.form.get('name')
    display_name = request.form.get('display_name')
    description = request.form.get('description')
    order = request.form.get('order', 0, type=int)

    category = GalleryCategory(
        name=name,
        display_name=display_name,
        description=description,
        order=order
    )
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('admin.gallery'))

@admin.route('/gallery/add_image', methods=['POST'])
@login_required
def add_gallery_image():
    if 'image' not in request.files:
        flash('Kein Bild ausgewählt', 'error')
        return redirect(url_for('admin.gallery'))
    
    file = request.files['image']
    if file.filename == '':
        flash('Kein Bild ausgewählt', 'error')
        return redirect(url_for('admin.gallery'))

    if file:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        file.save(os.path.join('static/uploads/gallery', filename))

        image = GalleryImage(
            title=request.form.get('title'),
            description=request.form.get('description'),
            image_path='uploads/gallery/' + filename,
            category_id=request.form.get('category_id', type=int),
            order=request.form.get('order', 0, type=int),
            is_outdoor=request.form.get('is_outdoor') == 'on',
            is_featured=request.form.get('is_featured') == 'on'
        )
        db.session.add(image)
        db.session.commit()

    return redirect(url_for('admin.gallery'))

@admin.route('/gallery/edit_image/<int:id>', methods=['POST'])
@login_required
def edit_gallery_image():
    image = GalleryImage.query.get_or_404(id)
    
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        file.save(os.path.join('static/uploads/gallery', filename))
        
        # Altes Bild löschen
        if image.image_path:
            old_path = os.path.join('static', image.image_path)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        image.image_path = 'uploads/gallery/' + filename

    image.title = request.form.get('title')
    image.description = request.form.get('description')
    image.category_id = request.form.get('category_id', type=int)
    image.order = request.form.get('order', 0, type=int)
    image.is_outdoor = request.form.get('is_outdoor') == 'on'
    image.is_featured = request.form.get('is_featured') == 'on'
    
    db.session.commit()
    return redirect(url_for('admin.gallery'))

@admin.route('/gallery/delete_image/<int:id>', methods=['POST'])
@login_required
def delete_gallery_image(id):
    image = GalleryImage.query.get_or_404(id)
    
    # Bild von der Festplatte löschen
    if image.image_path:
        file_path = os.path.join('static', image.image_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for('admin.gallery'))

@admin.route('/statistiken')
@login_required
def statistics():
    # 1. Stelle sicher, dass ein Eintrag für den heutigen Tag existiert
    today = datetime.now().date()
    
    today_entry = DailyStats.query.filter_by(date=today).first()
    if not today_entry:
        today_entry = DailyStats(date=today)
        db.session.add(today_entry)
        db.session.commit()

    # Finde das früheste Datum in der Datenbank (nach dem letzten Reset)
    earliest_entry = DailyStats.query.order_by(DailyStats.date.asc()).first()
    earliest_date = earliest_entry.date if earliest_entry else today
    
    # Verwende das früheste Datum statt automatisch 30 Tage zurück
    thirty_days_ago = earliest_date
    thirty_days_ago_datetime = datetime.combine(thirty_days_ago, datetime.min.time())

    # Die Statistiken ab dem frühesten Datum abfragen
    daily_stats = DailyStats.query.filter(
        DailyStats.date >= thirty_days_ago,
        DailyStats.date <= today
    ).order_by(DailyStats.date.desc()).all()

    # Berechne die Gesamtzahl der Besuche
    total_visits = sum(stat.total_visits for stat in daily_stats)

    # Berechne die durchschnittliche Verweildauer gewichtet nach der Anzahl der Besuche
    avg_duration = sum(stat.avg_duration * stat.total_visits for stat in daily_stats if stat.total_visits > 0) / total_visits if total_visits > 0 else 0
    
    # Cookie-Consent-Statistiken berechnen
    analytics_consents = db.session.query(func.count(PageVisit.id)).filter(PageVisit.analytics_consent == True).scalar() or 0
    total_page_visits = db.session.query(func.count(PageVisit.id)).scalar() or 0
    
    cookie_consent = {
        "necessary": total_page_visits,  # Alle Besuche haben notwendige Cookies
        "preferences": 0,  # Nicht im Modell verfügbar
        "analytics": analytics_consents,
        "marketing": 0,  # Nicht im Modell verfügbar
        "only_necessary": total_page_visits - analytics_consents  # Für das Diagramm benötigt
    }
    
    # Berechne tägliche eindeutige IP-Adressen
    daily_unique_ips = {}
    # Sammle alle IP-Adressen für jeden Tag
    daily_ip_addresses = {}
    
    # Sammle alle Besuche ab dem frühesten Datum
    page_visits_raw = PageVisit.query.filter(PageVisit.timestamp >= thirty_days_ago_datetime).all()
    
    # Gruppiere nach Datum und zähle eindeutige IPs
    for visit in page_visits_raw:
        date_str = visit.timestamp.strftime('%Y-%m-%d')
        if date_str not in daily_unique_ips:
            daily_unique_ips[date_str] = set()
            daily_ip_addresses[date_str] = []
        if visit.ip_address:  # Stelle sicher, dass die IP-Adresse vorhanden ist
            daily_unique_ips[date_str].add(visit.ip_address)
            if visit.ip_address not in daily_ip_addresses[date_str]:
                daily_ip_addresses[date_str].append(visit.ip_address)
    
    # Konvertiere Sets in Zahlen
    for date_str in daily_unique_ips:
        daily_unique_ips[date_str] = len(daily_unique_ips[date_str])

    # Browser-, Betriebssystem- und Gerätetyp-Statistiken
    browser_stats = {
        'chrome': sum(stat.chrome_users for stat in daily_stats),
        'firefox': sum(stat.firefox_users for stat in daily_stats),
        'safari': sum(stat.safari_users for stat in daily_stats),
        'edge': sum(stat.edge_users for stat in daily_stats),
        'other': sum(stat.other_browsers for stat in daily_stats)
    }

    os_stats = {
        'windows': sum(stat.windows_users for stat in daily_stats),
        'mac': sum(stat.mac_users for stat in daily_stats),
        'linux': sum(stat.linux_users for stat in daily_stats),
        'ios': sum(stat.ios_users for stat in daily_stats),
        'android': sum(stat.android_users for stat in daily_stats),
        'other': sum(stat.other_os for stat in daily_stats)
    }

    device_stats = {
        'desktop': sum(stat.desktop_users for stat in daily_stats),
        'mobile': sum(stat.mobile_users for stat in daily_stats)
    }

    # Seitenaufrufe nach Seiten sammeln
    page_visits = []
    system_visits = []  # Neue Liste für System-Aufrufe
    
    page_visits_query = db.session.query(
        PageVisit.page, 
        func.count(PageVisit.id).label('count')
    ).filter(
        PageVisit.timestamp >= thirty_days_ago_datetime
    ).group_by(
        PageVisit.page
    ).order_by(
        func.count(PageVisit.id).desc()
    ).all()

    for page_path, count in page_visits_query:
        friendly_name = get_friendly_page_name(page_path)
        
        # System-Aufrufe und API-Aufrufe ausfiltern/separieren
        if friendly_name and friendly_name.startswith("System:"):
            # Wir sammeln die System-Aufrufe, zeigen sie aber nicht an
            system_visits.append({
                'page': page_path,
                'friendly_name': friendly_name,
                'count': count
            })
        elif friendly_name:  # Nur Seiten mit gültigem Namen anzeigen
            page_visits.append({
                'page': page_path,
                'friendly_name': friendly_name,
                'count': count
            })
        else:
            # Fallback für den unwahrscheinlichen Fall, dass get_friendly_page_name None zurückgibt
            page_visits.append({
                'page': page_path,
                'friendly_name': "Unbekannte Seite",
                'count': count
            })

    # Galerieaufrufe nach Bildern sammeln
    gallery_views_query = db.session.query(
        GalleryView.image_id, 
        GalleryImage.title,
        func.count(GalleryView.id).label('count')
    ).join(
        GalleryImage, GalleryView.image_id == GalleryImage.id
    ).filter(
        GalleryView.timestamp >= thirty_days_ago_datetime
    ).group_by(
        GalleryView.image_id, GalleryImage.title
    ).order_by(
        func.count(GalleryView.id).desc()
    ).all()

    gallery_views = [{'image': title, 'count': count} for image_id, title, count in gallery_views_query]

    # Berechne die Gesamtzahl der Galerieaufrufe
    total_gallery_views = sum(view['count'] for view in gallery_views)
    
    # Berechne die Anzahl der eindeutigen Besucher (basierend auf IP-Adressen)
    unique_visitors = sum(len(ips) for ips in daily_unique_ips.values() if isinstance(ips, set))
    if not unique_visitors:  # Falls daily_unique_ips bereits in Zahlen konvertiert wurde
        unique_visitors = sum(daily_unique_ips.values())
    
    # Paginierung für tägliche Statistiken
    page = request.args.get('page', type=int, default=1)
    per_page = 10
    
    # Paginierung für tägliche Statistiken - korrigiert
    total_days = len(daily_stats)
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_days)
    
    paginated_stats = daily_stats[start_idx:end_idx]
    
    pagination = Pagination(
        page=page,
        total=total_days,
        per_page=per_page,
        css_framework='bootstrap4',
        prev_label='Zurück',
        next_label='Weiter',
        record_name='Tage'
    )
    
    # Wir übergeben eine leere Datenstruktur, damit die Templates funktionieren
    page_visits_by_date = {}
    
    return render_template(
        'admin/statistics.html',
        daily_stats=paginated_stats,  # Nur die paginierten Statistiken senden
        page_visits=page_visits,
        browser_stats=browser_stats,
        os_stats=os_stats,
        device_stats=device_stats,
        gallery_views=gallery_views,
        total_entries=total_days,
        pagination=pagination,
        total_visits=total_visits,
        cookie_consent=cookie_consent,
        daily_unique_ips=daily_unique_ips,
        daily_ip_addresses=daily_ip_addresses,  # Neue Variable für IP-Adressen
        thirty_days_ago=thirty_days_ago,
        unique_visitors=unique_visitors,
        total_gallery_views=total_gallery_views,
        avg_duration=avg_duration,
        page_visits_by_date=page_visits_by_date,
        current_date=today  # Aktuelles Datum hinzufügen
    )

@admin.route('/statistiken/reset', methods=['POST'])
@login_required
def reset_statistics():
    """Setzt alle Statistiken zurück."""
    try:
        if current_user.username != 'admin':
            flash('Nur der Administrator kann die Statistiken zurücksetzen.', 'danger')
            return redirect(url_for('admin.statistics'))
            
        # Statistiken löschen - ALLE Einträge, nicht nur die neuesten
        db.session.query(DailyStats).delete()
        db.session.query(PageVisit).delete()
        db.session.query(GalleryView).delete()
        
        # Nur den heutigen Tag initialisieren
        today = datetime.now().date()
        today_entry = DailyStats(
            date=today,
            total_visits=0,
            unique_visitors=0,
            gallery_views=0,
            avg_duration=0,
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
        db.session.add(today_entry)
        
        db.session.commit()
        
        flash('Alle Statistiken wurden erfolgreich zurückgesetzt.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Zurücksetzen der Statistiken: {str(e)}', 'danger')
    
    return redirect(url_for('admin.statistics'))

@admin.route('/menu/add', methods=['POST'])
@login_required
def add_menu_item():
    try:
        data = request.get_json()
        
        # Überprüfe, ob alle erforderlichen Felder vorhanden sind
        required_fields = ['name', 'description', 'price', 'category_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Feld {field} fehlt'}), 400
        
        # Erstelle ein neues MenuItem
        item = MenuItem(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            category_id=int(data['category_id']),
            order=data.get('order', 0)  # Optional, Standard ist 0
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'item': {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'category_id': item.category_id,
                'order': item.order
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin.route('/menu/delete/<int:id>', methods=['POST'])
@login_required
def delete_menu_item(id):
    try:
        item = MenuItem.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        flash('Item wurde erfolgreich gelöscht.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Fehler beim Löschen des Items.', 'error')
    return redirect(url_for('admin.menu'))

@admin.route('/menu/edit/<int:id>', methods=['GET'])
@login_required
def edit_menu_item(id):
    try:
        item = MenuItem.query.get_or_404(id)
        return jsonify({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'category_id': item.category_id,
            'vegetarian': item.vegetarian,
            'vegan': item.vegan,
            'spicy': item.spicy,
            'gluten_free': item.gluten_free,
            'lactose_free': item.lactose_free,
            'kid_friendly': item.kid_friendly,
            'alcohol_free': item.alcohol_free,
            'contains_alcohol': item.contains_alcohol,
            'homemade': item.homemade,
            'sugar_free': item.sugar_free,
            'recommended': item.recommended,
            'image_path': item.image_path if item.image_path else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin.route('/menu/edit', methods=['POST'])
@login_required
def edit_menu_item_post():
    form = FlaskForm()  # Create a form instance for CSRF token
    if form.validate_on_submit():
        try:
            item_id = request.form.get('id')
            item = MenuItem.query.get_or_404(item_id)
            
            item.name = request.form.get('name')
            item.description = request.form.get('description')
            item.price = float(request.form.get('price'))
            item.category_id = int(request.form.get('category'))
            
            # Handle image upload if provided
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    # Delete old image if exists
                    if item.image_path:
                        old_path = os.path.join(current_app.root_path, 'static', item.image_path)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    
                    # Save new image
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    new_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
                    file.save(filepath)
                    
                    # Update database with new image path
                    item.image_path = os.path.join('uploads', new_filename).replace('\\', '/')
            
            # Handle image removal
            if request.form.get('remove_image') == 'true' and item.image_path:
                old_path = os.path.join(current_app.root_path, 'static', item.image_path)
                if os.path.exists(old_path):
                    os.remove(old_path)
                item.image_path = None
            
            # Update boolean fields
            item.vegetarian = 'vegetarian' in request.form
            item.vegan = 'vegan' in request.form
            item.spicy = 'spicy' in request.form
            item.gluten_free = 'gluten_free' in request.form
            item.lactose_free = 'lactose_free' in request.form
            item.kid_friendly = 'kid_friendly' in request.form
            item.alcohol_free = 'alcohol_free' in request.form
            item.contains_alcohol = 'contains_alcohol' in request.form
            item.homemade = 'homemade' in request.form
            item.sugar_free = 'sugar_free' in request.form
            item.recommended = 'recommended' in request.form
            
            db.session.commit()
            flash('Menüpunkt wurde erfolgreich aktualisiert!', 'success')
            return redirect(url_for('admin.menu'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Aktualisieren des Menüpunkts: {str(e)}', 'error')
            return redirect(url_for('admin.menu'))
    
    return redirect(url_for('admin.menu'))

# Alte Route weiterleiten
@admin.route('/opening-hours/add', methods=['POST'])
@login_required
def add_opening_hours_redirect():
    return redirect(url_for('admin.add_opening_hours'))

# Alte Route weiterleiten
@admin.route('/opening-hours/<int:id>', methods=['GET'])
@login_required
def get_opening_hours_redirect(id):
    return redirect(url_for('admin.get_opening_hours', id=id))

# Alte Route weiterleiten
@admin.route('/opening-hours/edit/<int:id>', methods=['POST'])
@login_required
def edit_opening_hours_redirect(id):
    return redirect(url_for('admin.edit_opening_hours', id=id))

# Alte Route weiterleiten
@admin.route('/opening-hours/delete/<int:id>', methods=['POST'])
@login_required
def delete_opening_hours_redirect(id):
    return redirect(url_for('admin.delete_opening_hours', id=id))

# Alte Route weiterleiten
@admin.route('/opening-hours')
@login_required
def opening_hours_redirect():
    return redirect(url_for('admin.opening_hours'))

# Alte Route weiterleiten
@admin.route('/statistics')
@login_required
def statistics_redirect():
    return redirect(url_for('admin.statistics'))
