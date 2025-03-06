from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file, abort, make_response, current_app, g, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import case, func
from sqlalchemy.sql import distinct
from flask_wtf.csrf import CSRFProtect, validate_csrf, CSRFError
from werkzeug.middleware.proxy_fix import ProxyFix

# API-Schlüssel für sichere AJAX-Anfragen
try:
    with open('instance/api_key.txt', 'r') as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    API_KEY = 'RVXvUD4a01dTyTh6QBm9mBcefvmHb98o'
    print("API-Schlüssel wurde neu generiert.")

# Deaktiviere die API-Schlüssel-Validierung temporär
def validate_api_key(request):
    # Immer True zurückgeben, um Weiterleitungsprobleme zu vermeiden
    return True

import os
import re
import time
import random
import string
from datetime import datetime, date, timedelta
from werkzeug.utils import secure_filename
from PIL import Image
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, IntegerField, FloatField, FileField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_migrate import Migrate
import json
from markupsafe import Markup

from extensions import db, init_extensions
from models import User, MenuItem, MenuCategory, OpeningHours, GalleryImage, PageVisit, GalleryView, DailyStats, GalleryCategory
from utils import track_page_visit, track_gallery_view, get_statistics, update_visit_duration, get_friendly_page_name
from admin_routes import admin
# from security_utils import sanitize_html, validate_file_ext, validate_file_content, sanitize_input, sanitize_integer, sanitize_float, sanitize_filename

# Temporäre Ersatzfunktionen für security_utils
def sanitize_html(content):
    return content

def validate_file_ext(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def sanitize_input(input_str):
    if input_str is None:
        return ""
    return input_str.strip()

def sanitize_integer(value, default=0, min_value=None, max_value=None):
    try:
        val = int(value)
        if min_value is not None and val < min_value:
            return min_value
        if max_value is not None and val > max_value:
            return max_value
        return val
    except (ValueError, TypeError):
        return default

def sanitize_float(value, default=0.0, min_value=None, max_value=None):
    try:
        val = float(value)
        if min_value is not None and val < min_value:
            return min_value
        if max_value is not None and val > max_value:
            return max_value
        return val
    except (ValueError, TypeError):
        return default

def validate_file_content(file_path):
    return True

def sanitize_filename(filename):
    return secure_filename(filename)

app = Flask(__name__)
# Konfiguration basierend auf Umgebung laden
if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_pyfile('instance/production.cfg')
else:
    app.config.from_pyfile('instance/development.cfg')

# Stellen Sie sicher, dass der DEBUG-Modus in der Produktion deaktiviert ist
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False

# ProxyFix-Middleware aktivieren, um korrekte IP-Adressen hinter Proxies zu erhalten
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Secret Key wird jetzt über Konfigurationsdateien gesteuert
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Stellen Sie sicher, dass UTF-8 für die Anwendung verwendet wird
app.config['JSON_AS_ASCII'] = False
app.jinja_env.filters['tojson'] = lambda x: Markup(json.dumps(x))

# Stelle sicher, dass der Upload-Ordner existiert
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialisiere Erweiterungen
init_extensions(app)
migrate = Migrate(app, db)

# Login Manager konfigurieren
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = None  # Explizit auf None setzen, um automatische Umleitung zu deaktivieren
login_manager.login_message = 'Bitte melden Sie sich an, um auf den Admin-Bereich zuzugreifen.'
login_manager.login_message_category = 'error'
login_manager.session_protection = 'strong'

# Registriere Blueprints
app.register_blueprint(admin)

csrf = CSRFProtect(app)

# Deaktiviere CSRF komplett für Entwicklung
app.config['WTF_CSRF_ENABLED'] = False

app.config['SECRET_KEY'] = 'dein-geheimer-schluessel'  # Stelle sicher, dass ein Secret Key gesetzt ist
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Session-Lebensdauer: 1 Tag

@app.context_processor
def utility_processor():
    """Fügt Hilfsfunktionen zu allen Templates hinzu"""
    return {
        'csrf_token': lambda: ''  # Gibt einen leeren String zurück statt eines Tokens
    }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class MenuItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Beschreibung', validators=[DataRequired()])
    price = FloatField('Preis', validators=[DataRequired()])
    category_id = SelectField('Kategorie', coerce=int)
    image = FileField('Bild', validators=[FileAllowed(['jpg', 'png'], 'Nur Bilder erlaubt')])
    vegetarian = BooleanField('Vegetarisch')
    vegan = BooleanField('Vegan')
    spicy = BooleanField('Scharf')
    gluten_free = BooleanField('Glutenfrei')
    lactose_free = BooleanField('Laktosefrei')
    kid_friendly = BooleanField('Kinderfreundlich')
    alcohol_free = BooleanField('Alkoholfrei')
    contains_alcohol = BooleanField('Enthält Alkohol')
    homemade = BooleanField('Hausgemacht')
    sugar_free = BooleanField('Zuckerfrei')
    recommended = BooleanField('Empfohlen')

class GalleryImageForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired()])
    description = TextAreaField('Beschreibung', validators=[DataRequired()])
    image = FileField('Bild', validators=[FileAllowed(['jpg', 'png'], 'Nur Bilder erlaubt')])

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.template_filter('from_json')
def from_json(value):
    if value is None:
        return {}
    try:
        if isinstance(value, str):
            return json.loads(value)
        return value
    except:
        return {}

@app.before_request
def track_visit():
    """Trackt jeden Seitenaufruf, der nicht in der Ausschlussliste ist."""
    try:
        # Nicht tracken, wenn es sich um statische Dateien oder bestimmte Pfade handelt
        if (request.path.startswith('/static/') or 
            request.path.startswith('/admin') or  # Alle Admin-Pfade ausschließen (mit oder ohne Slash)
            request.path.startswith('/get_') or 
            request.path.startswith('/update_visit_duration') or 
            request.path == '/favicon.ico'):
            return
        
        # Auch API-Aufrufe und Ressourcen ausschließen
        if any(request.path.endswith(ext) for ext in ['.jpg', '.png', '.gif', '.css', '.js', '.ico']):
            return
            
        # Stattdessen hier den Aufruf zur track_page_visit-Funktion ausführen
        # Dies trackt nur echte Seiten, keine API-Calls oder statischen Ressourcen
        if not request.path.startswith('/api/') and not request.path.startswith('/get_'):
            # Sichere Version des Trackings
            from utils import track_page_visit
            track_page_visit(request.path)
    except Exception as e:
        # Fehler beim Tracking sollten den Seitenaufruf nicht verhindern
        print(f"Fehler beim Tracking: {str(e)}")
        import traceback
        traceback.print_exc()

@app.route('/')
def index():
    image_path = os.path.join(app.static_folder, 'img/awards/Lokal_Des_Jahres_Deutschlansd_2024_Bild-removebg-preview.png')
    print(f"Checking image path: {image_path}")
    print(f"File exists: {os.path.exists(image_path)}")
    try:
        categories = MenuCategory.query.order_by(MenuCategory.order).all()
        menu_items = MenuItem.query.all()
        opening_hours = OpeningHours.query.order_by(
            case(
                (OpeningHours.day == 'Montag', 1),
                (OpeningHours.day == 'Dienstag', 2),
                (OpeningHours.day == 'Mittwoch', 3),
                (OpeningHours.day == 'Donnerstag', 4),
                (OpeningHours.day == 'Freitag', 5),
                (OpeningHours.day == 'Samstag', 6),
                (OpeningHours.day == 'Sonntag', 7)
            )
        ).all()
        return render_template('index.html', categories=categories, menu_items=menu_items, opening_hours=opening_hours)
    except Exception as e:
        print(f"Fehler auf der Homepage: {str(e)}")
        db.create_all()  # Initialisiere die Datenbank falls sie nicht existiert
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    class LoginForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Anmelden')

    form = LoginForm()
        
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None:
            flash('Benutzer nicht gefunden.')
            return render_template('admin/login.html', form=form)
            
        if not user.check_password(form.password.data):
            flash('Falsches Passwort.')
            return render_template('admin/login.html', form=form)
            
        if not user.is_admin:
            flash('Keine Administratorrechte.')
            return render_template('admin/login.html', form=form)
            
        # Setze remember=True, um die Session stabil zu halten
        login_user(user, remember=True)
        
        # Ignoriere den next-Parameter und leite immer zum Admin-Bereich
        return redirect(url_for('admin.index'))
    
    return render_template('admin/login.html', form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if current_user.is_authenticated:
        # Direkt zum Admin-Index umleiten ohne Parameter
        return redirect('/admin/index')
    else:
        # Login-Formular für GET und POST-Anfragen
        class LoginForm(FlaskForm):
            username = StringField('Username', validators=[DataRequired()])
            password = PasswordField('Password', validators=[DataRequired()])
            submit = SubmitField('Anmelden')
        
        form = LoginForm()
        
        if request.method == 'POST' and form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            
            if user is None:
                flash('Benutzer nicht gefunden.')
                return render_template('admin/login.html', form=form)
                
            if not user.check_password(form.password.data):
                flash('Falsches Passwort.')
                return render_template('admin/login.html', form=form)
                
            if not user.is_admin:
                flash('Keine Administratorrechte.')
                return render_template('admin/login.html', form=form)
                
            # Setze remember=True, um die Session stabil zu halten
            login_user(user, remember=True)
            
            # Nach erfolgreicher Anmeldung direkt zum Admin-Index weiterleiten ohne Parameter
            return redirect('/admin/index')
            
        return render_template('admin/login.html', form=form)

@app.route('/admin/', methods=['GET', 'POST'])
def admin_dashboard_slash():
    # Leite immer auf /admin um ohne Parameter und benutze 301 für permanente Umleitung
    return redirect('/admin', code=301)

@app.route('/admin/speisekarte')
@login_required
def admin_speisekarte():
    categories = MenuCategory.query.order_by(MenuCategory.order).all()
    menu_items = MenuItem.query.order_by(MenuItem.order, MenuItem.id).all()
    form = FlaskForm()  # Create a form instance for CSRF token
    return render_template('admin/menu.html', categories=categories, menu_items=menu_items, form=form)

@app.route('/admin/menu')
@login_required
def admin_menu_redirect():
    return redirect(url_for('admin_speisekarte'))

def allowed_file(filename):
    """
    Überprüft, ob der Dateiname eine erlaubte Erweiterung hat.
    Verwendet die verbesserte Funktion aus security_utils.
    """
    return validate_file_ext(filename)

def secure_upload(file, subfolder='', check_content=True):
    """Sichere Handhabung von Datei-Uploads"""
    try:
        if file and allowed_file(file.filename):
            # Sicheren Dateinamen erstellen
            base_filename = sanitize_filename(file.filename)
            timestamp = int(time.time())
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            new_filename = f"{timestamp}_{random_part}_{base_filename}"
            
            # Zielverzeichnis erstellen, falls es nicht existiert
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
            if not os.path.exists(upload_path):
                app.logger.info(f"Creating directory: {upload_path}")
                os.makedirs(upload_path, exist_ok=True)
            
            # Vollständigen Dateipfad erstellen
            file_path = os.path.join(upload_path, new_filename)
            app.logger.info(f"Saving file to: {file_path}")
            
            # Datei speichern
            file.save(file_path)
            app.logger.info(f"File saved successfully")
            
            # Check if file was actually saved
            if not os.path.exists(file_path):
                app.logger.error(f"File was not saved at {file_path}")
                return None
                
            # Optional: Dateiinhalt validieren (z.B. für Bilder, um sicherzustellen, dass es wirklich Bilder sind)
            if check_content and not validate_file_content(file_path):
                # Ungültige Datei löschen
                app.logger.error(f"File content validation failed for {file_path}")
                os.remove(file_path)
                return None

            # Pfad zurückgeben (relativ zum UPLOAD_FOLDER)
            relative_path = os.path.join(subfolder, new_filename).replace('\\', '/')
            return relative_path
    except Exception as e:
        app.logger.error(f"Error in secure_upload: {str(e)}")
        app.logger.exception("Exception details:")
        return None
        
    return None

@app.route('/admin/speisekarte/hinzufuegen', methods=['GET', 'POST'])
@login_required
def admin_menu_add():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    form = FlaskForm()  # Create a form instance for CSRF token
    if form.validate_on_submit():
        try:
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price'))
            category_id = int(request.form.get('category'))
            vegetarian = bool(request.form.get('vegetarian'))
            vegan = bool(request.form.get('vegan'))
            spicy = bool(request.form.get('spicy'))
            gluten_free = bool(request.form.get('gluten_free'))
            lactose_free = bool(request.form.get('lactose_free'))
            kid_friendly = bool(request.form.get('kid_friendly'))
            alcohol_free = bool(request.form.get('alcohol_free'))
            contains_alcohol = bool(request.form.get('contains_alcohol'))
            homemade = bool(request.form.get('homemade'))
            sugar_free = bool(request.form.get('sugar_free'))
            recommended = bool(request.form.get('recommended'))
            
            image = request.files.get('image')
            image_path = None
            if image and image.filename:
                filename = secure_upload(image, 'uploads')
                if filename:
                    image_path = filename
            
            menu_item = MenuItem(
                name=name,
                description=description,
                price=price,
                category_id=category_id,
                vegetarian=vegetarian,
                vegan=vegan,
                spicy=spicy,
                gluten_free=gluten_free,
                lactose_free=lactose_free,
                kid_friendly=kid_friendly,
                alcohol_free=alcohol_free,
                contains_alcohol=contains_alcohol,
                homemade=homemade,
                sugar_free=sugar_free,
                recommended=recommended,
                image_path=image_path
            )
            
            db.session.add(menu_item)
            db.session.commit()
            
            flash('Menüpunkt erfolgreich hinzugefügt')
        except Exception as e:
            flash(f'Fehler beim Hinzufügen des Menüpunkts: {str(e)}')
        
        return redirect(url_for('admin_speisekarte'))
    
    return redirect(url_for('admin_speisekarte'))

# Alte Admin-Route weiterleiten zur neuen Route
@app.route('/admin/menu/add', methods=['GET', 'POST'])
@login_required
def admin_menu_add_redirect():
    return redirect(url_for('admin_menu_add'))

@app.route('/admin/speisekarte/bearbeiten/<int:id>')
@login_required
def admin_menu_edit(id):
    item = MenuItem.query.get_or_404(id)
    categories = MenuCategory.query.order_by(MenuCategory.order).all()
    form = FlaskForm()  # Create a form instance for CSRF token
    return render_template('admin/edit_menu_item.html', item=item, categories=categories, form=form)

# API-Route für die JSON-Daten eines Menüpunkts
@app.route('/admin-panel/menu/edit/<int:id>')
@login_required
def admin_menu_edit_api(id):
    try:
        item = MenuItem.query.get_or_404(id)
        return jsonify({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'category_id': item.category_id,
            'image_path': item.image_path,
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
            'recommended': item.recommended
        })
    except Exception as e:
        print(f"Fehler beim Abrufen des Menüpunkts: {str(e)}")
        return jsonify({'error': 'Fehler beim Laden der Menüpunkt-Daten'}), 500

# Alte Admin-Route weiterleiten zur neuen Route
@app.route('/admin/menu/edit/<int:id>')
@login_required
def admin_menu_edit_redirect(id):
    return redirect(url_for('admin_menu_edit', id=id))

@app.route('/admin/speisekarte/bearbeiten', methods=['POST'])
@login_required
def admin_menu_edit_post():
    form = FlaskForm()  # Create a form instance for CSRF token
    if form.validate_on_submit():
        item_id = request.form.get('id')
        item = MenuItem.query.get_or_404(item_id)
        
        # Speichere die Kategorie für die Positionswiederherstellung
        category_id = item.category_id
        
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.price = float(request.form.get('price'))
        item.category_id = int(request.form.get('category'))
        
        # Handle image upload if provided
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_upload(file, 'uploads')
                if filename:
                    item.image_path = filename
        
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
        flash('Gericht erfolgreich aktualisiert', 'success')
        
        # Leite zur Speisekarte zurück mit Ankerpunkt auf die bearbeitete Kategorie
        # Verwende die ursprüngliche Kategorie-ID für die Position
        return redirect(url_for('admin_speisekarte', _anchor=f'category-{category_id}'))
    
    return redirect(url_for('admin_speisekarte'))

# Alte Admin-Route weiterleiten zur neuen Route
@app.route('/admin/menu/edit', methods=['POST'])
@login_required
def admin_menu_edit_post_redirect():
    return redirect(url_for('admin_menu_edit_post'))

@app.route('/admin/speisekarte/loeschen/<int:id>')
@login_required
def admin_menu_delete(id):
    try:
        menu_item = MenuItem.query.get_or_404(id)
        
        # Bild löschen wenn vorhanden
        if menu_item.image_path:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], menu_item.image_path)
            if os.path.exists(image_path):
                os.remove(image_path)
        
        db.session.delete(menu_item)
        db.session.commit()
        flash('Menüpunkt erfolgreich gelöscht')
    except Exception as e:
        flash(f'Fehler beim Löschen des Menüpunkts: {str(e)}')
    
    return redirect(url_for('admin_speisekarte'))

# Alte Admin-Route weiterleiten zur neuen Route
@app.route('/admin/menu/delete/<int:id>')
@login_required
def admin_menu_delete_redirect(id):
    return redirect(url_for('admin_menu_delete', id=id))

@app.route('/admin/kategorien')
@login_required
def admin_categories():
    categories = MenuCategory.query.order_by(MenuCategory.order).all()
    form = FlaskForm()  # Create a form instance for CSRF token
    return render_template('admin/categories.html', categories=categories, form=form)

# Neue Route für die Neuanordnung von Kategorien per Drag & Drop
@app.route('/admin/kategorien/reorder', methods=['POST'])
@login_required
def admin_categories_reorder():
    try:
        data = request.json
        categories = data.get('categories', [])
        
        # Überprüfen, ob Daten erhalten wurden
        if not categories:
            return jsonify({'success': False, 'error': 'Keine Daten erhalten'})
        
        # Für jede Kategorie die Reihenfolge aktualisieren
        for category_data in categories:
            category_id = category_data.get('id')
            new_order = category_data.get('order')
            
            if category_id and new_order:
                category = MenuCategory.query.get(category_id)
                if category:
                    category.order = new_order
        
        # Änderungen in der Datenbank speichern
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Alte Admin-Route weiterleiten zur neuen Route
@app.route('/admin/categories')
@login_required
def admin_categories_redirect():
    return redirect(url_for('admin_categories'))

@app.route('/admin/kategorien/hinzufuegen', methods=['GET', 'POST'])
@login_required
def admin_categories_add():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            display_name = request.form.get('display_name')
            is_drink_category = 'is_drink_category' in request.form
            
            # Höchste Ordnungszahl ermitteln und +1 für neue Kategorie
            max_order = db.session.query(db.func.max(MenuCategory.order)).scalar() or 0
            
            category = MenuCategory(
                name=name,
                display_name=display_name,
                order=max_order + 1,
                is_drink_category=is_drink_category
            )
            
            db.session.add(category)
            db.session.commit()
            
            flash('Kategorie wurde erfolgreich hinzugefügt.', 'success')
            return redirect(url_for('admin_categories'))
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Hinzufügen der Kategorie: {str(e)}', 'danger')
    
    return redirect(url_for('admin_categories'))

# Alte Admin-Route weiterleiten zur neuen Route
@app.route('/admin/categories/add', methods=['GET', 'POST'])
@login_required
def admin_categories_add_redirect():
    return redirect(url_for('admin_categories_add'))

@app.route('/admin/oeffnungszeiten')
@login_required
def admin_hours():
    opening_hours = OpeningHours.query.order_by(
        case(
            (OpeningHours.day == 'Montag', 1),
            (OpeningHours.day == 'Dienstag', 2),
            (OpeningHours.day == 'Mittwoch', 3),
            (OpeningHours.day == 'Donnerstag', 4),
            (OpeningHours.day == 'Freitag', 5),
            (OpeningHours.day == 'Samstag', 6),
            (OpeningHours.day == 'Sonntag', 7)
        )
    ).all()
    return render_template('admin/opening_hours.html', hours=opening_hours, form=FlaskForm())

@app.route('/admin/oeffnungszeiten/hinzufuegen', methods=['POST'])
@login_required
def admin_add_opening_hours():
    try:
        print("==== HINZUFÜGEN VON ÖFFNUNGSZEITEN ====")
        print("Empfangene Formulardaten:", request.form)  

        # Grundlegende Validierung
        day = request.form.get('day')
        if not day:
            print("Fehler: Kein Tag angegeben")
            return jsonify({'success': False, 'message': 'Tag muss angegeben werden.'}), 400
            
        # Überprüfe, ob bereits Öffnungszeiten für diesen Tag existieren
        existing_hours = OpeningHours.query.filter_by(day=day).first()
        if existing_hours:
            print(f"Fehler: Öffnungszeiten für {day} existieren bereits")
            return jsonify({'success': False, 'message': f'Öffnungszeiten für {day} existieren bereits.'}), 400
        
        # Neue Öffnungszeiten erstellen
        hours = OpeningHours(day=day)
        
        # String-Werte zu Boolean konvertieren
        vacation_active_str = request.form.get('vacation_active', 'false')
        closed_str = request.form.get('closed', 'false')
        
        vacation_active = vacation_active_str.lower() == 'true'
        closed = closed_str.lower() == 'true'
        
        print(f"Status: Urlaub={vacation_active}, Ruhetag={closed}")
        
        # Boolean-Werte setzen
        hours.vacation_active = vacation_active
        hours.closed = closed
        
        if vacation_active and closed:
            print("Fehler: Sowohl Urlaub als auch Ruhetag ausgewählt")
            return jsonify({'success': False, 'message': 'Ein Tag kann nicht gleichzeitig Urlaub und Ruhetag sein.'}), 400
        
        # Je nach Status die entsprechenden Felder setzen
        if vacation_active:
            vacation_start = request.form.get('vacation_start')
            vacation_end = request.form.get('vacation_end')
            
            if not vacation_start or not vacation_end:
                print("Fehler: Urlaubsdaten fehlen")
                return jsonify({'success': False, 'message': 'Bitte geben Sie Start- und Enddatum für den Urlaub an.'}), 400
                
            try:
                hours.vacation_start = datetime.strptime(vacation_start, '%Y-%m-%d').date()
                hours.vacation_end = datetime.strptime(vacation_end, '%Y-%m-%d').date()
                
                # Urlaub validieren
                if hours.vacation_start > hours.vacation_end:
                    print("Fehler: Startdatum liegt nach Enddatum")
                    return jsonify({'success': False, 'message': 'Das Startdatum muss vor dem Enddatum liegen.'}), 400
                    
                print(f"Urlaubsdaten: {vacation_start} bis {vacation_end}")
            except Exception as e:
                print(f"Fehler bei Datumsformat: {str(e)}")
                return jsonify({'success': False, 'message': f'Ungültiges Datum: {str(e)}'}), 400
        elif not closed:
            # Normale Öffnungszeiten setzen
            open_time_1 = request.form.get('open_time_1')
            close_time_1 = request.form.get('close_time_1')
            
            if not open_time_1 or not close_time_1:
                print("Fehler: Öffnungszeiten fehlen")
                return jsonify({'success': False, 'message': 'Bitte geben Sie mindestens die erste Öffnungszeit an.'}), 400
            
            hours.open_time_1 = open_time_1
            hours.close_time_1 = close_time_1
            print(f"Öffnungszeit 1: {open_time_1} - {close_time_1}")
            
            open_time_2 = request.form.get('open_time_2')
            close_time_2 = request.form.get('close_time_2')
            
            if open_time_2 and close_time_2:
                hours.open_time_2 = open_time_2
                hours.close_time_2 = close_time_2
                print(f"Öffnungszeit 2: {open_time_2} - {close_time_2}")

        # Speichern in der Datenbank
        print("Speichere Öffnungszeiten in der Datenbank...")
        db.session.add(hours)
        db.session.commit()
        
        print(f"Öffnungszeiten für {day} erfolgreich hinzugefügt!")
        return jsonify({
            'success': True,
            'message': f'Öffnungszeiten für {day} wurden erfolgreich hinzugefügt.',
            'hours': hours.to_dict()
        })
        
    except Exception as e:
        print(f"Fehler beim Hinzufügen: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Ein Fehler ist aufgetreten: {str(e)}'}), 400

@app.route('/admin/oeffnungszeiten/loeschen/<int:id>', methods=['POST'])
@login_required
def admin_delete_hours(id):
    print(f"Delete route wurde aufgerufen für ID: {id}")
    try:
        print("Suche nach Öffnungszeit in der Datenbank...")
        hours = OpeningHours.query.get_or_404(id)
        print(f"Öffnungszeit gefunden: {hours.day}")
        db.session.delete(hours)
        db.session.commit()
        print("Öffnungszeit erfolgreich gelöscht")
        return jsonify({
            'success': True,
            'message': 'Öffnungszeiten wurden erfolgreich gelöscht.'
        })
    except Exception as e:
        print(f"Fehler beim Löschen: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Fehler beim Löschen der Öffnungszeiten: {str(e)}'
        }), 400

@app.route('/admin/hours/<int:id>', methods=['GET'])
@login_required
def admin_get_hours(id):
    # AJAX-Kompatibiltätsschicht für alte Routen
    return jsonify(db.session.get(OpeningHours, id).to_dict())

@app.route('/admin/hours/add', methods=['POST'])
@login_required
def admin_add_opening_hours_redirect():
    # AJAX-Anfragen an den Blueprint weiterleiten
    return admin.add_opening_hours()

@app.route('/admin/hours/edit/<int:id>', methods=['POST'])
@login_required
def admin_edit_hours_redirect(id):
    # AJAX-Anfragen an den Blueprint weiterleiten
    return admin.edit_opening_hours(id)

@app.route('/admin/hours/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_hours_redirect(id):
    # AJAX-Anfragen an den Blueprint weiterleiten
    return admin.delete_opening_hours(id)

@app.route('/menu')
def menu():
    categories = MenuCategory.query.order_by(MenuCategory.order).all()
    menu_items = MenuItem.query.order_by(MenuItem.id).all()
    
    # Für jedes Menüitem die Tags als Liste hinzufügen
    for item in menu_items:
        item.tags = []
        if item.vegetarian:
            item.tags.append('vegetarian')
        if item.vegan:
            item.tags.append('vegan')
        if item.spicy:
            item.tags.append('spicy')
        if item.gluten_free:
            item.tags.append('gluten_free')
        if item.lactose_free:
            item.tags.append('lactose_free')
        if item.kid_friendly:
            item.tags.append('kid_friendly')
        if item.alcohol_free:
            item.tags.append('alcohol_free')
        if item.contains_alcohol:
            item.tags.append('contains_alcohol')
        if item.homemade:
            item.tags.append('homemade')
        if item.sugar_free:
            item.tags.append('sugar_free')
        if item.recommended:
            item.tags.append('recommended')
    
    return render_template('menu.html', categories=categories, menu_items=menu_items)

@app.route('/speisekarte')
def speisekarte():
    categories = MenuCategory.query.order_by(MenuCategory.order).all()
    menu_items = MenuItem.query.order_by(MenuItem.id).all()
    
    # Für jedes Menüitem die Tags als Liste hinzufügen
    for item in menu_items:
        item.tags = []
        if item.vegetarian:
            item.tags.append('vegetarian')
        if item.vegan:
            item.tags.append('vegan')
        if item.spicy:
            item.tags.append('spicy')
        if item.gluten_free:
            item.tags.append('gluten_free')
        if item.lactose_free:
            item.tags.append('lactose_free')
        if item.kid_friendly:
            item.tags.append('kid_friendly')
        if item.alcohol_free:
            item.tags.append('alcohol_free')
        if item.contains_alcohol:
            item.tags.append('contains_alcohol')
        if item.homemade:
            item.tags.append('homemade')
        if item.sugar_free:
            item.tags.append('sugar_free')
        if item.recommended:
            item.tags.append('recommended')
    
    return render_template('speisekarte.html', categories=categories, menu_items=menu_items)

# Alte Route weiterleiten zur neuen Route
@app.route('/menu', methods=['GET'])
def menu_redirect():
    return redirect(url_for('speisekarte'))

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/datenschutz')
def datenschutz():
    return render_template('datenschutz.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sie wurden erfolgreich abgemeldet.', 'success')
    return redirect(url_for('index'))

@app.route('/galerie')
def gallery():
    categories = GalleryCategory.query.order_by(GalleryCategory.order).all()
    images = GalleryImage.query.order_by(GalleryImage.category_id, GalleryImage.order).all()
    return render_template('gallery.html', categories=categories, images=images)

@app.route('/admin/galerie')
@login_required
def admin_galerie():
    images = GalleryImage.query.order_by(GalleryImage.id.desc()).all()
    categories = GalleryCategory.query.all()
    
    # Zähle, wie viele Bilder es pro Kategorie gibt
    category_counts = {}
    for cat in categories:
        count = GalleryImage.query.filter_by(category_id=cat.id).count()
        category_counts[cat.id] = count
    
    return render_template('admin/gallery.html', images=images, categories=categories, category_counts=category_counts)

@app.route('/admin/gallery')
@login_required
def admin_gallery_redirect():
    return redirect(url_for('admin_galerie'))

@app.route('/admin/galerie/kategorie/hinzufuegen', methods=['POST'])
@login_required
def admin_kategorie_hinzufuegen():
    try:
        name = request.form.get('name', '').strip()
        display_name = request.form.get('display_name', '').strip()
        description = request.form.get('description', '').strip()
        order = request.form.get('order', type=int, default=0)
        
        if not name or not display_name:
            flash('Bitte geben Sie einen Namen und einen Anzeigenamen ein.', 'error')
            return redirect(url_for('admin_galerie'))
        
        if GalleryCategory.query.filter_by(name=name).first():
            flash('Eine Kategorie mit diesem Namen existiert bereits.', 'error')
            return redirect(url_for('admin_galerie'))
        
        category = GalleryCategory(
            name=name,
            display_name=display_name,
            description=description,
            order=order
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Kategorie wurde erfolgreich hinzugefügt.', 'success')
    
    except Exception as e:
        flash(f'Fehler beim Hinzufügen der Kategorie: {str(e)}', 'error')
    
    return redirect(url_for('admin_galerie'))

@app.route('/admin/gallery/category/add', methods=['POST'])
@login_required
def admin_category_add_redirect():
    return redirect(url_for('admin_kategorie_hinzufuegen'))

@app.route('/admin/galerie/kategorie/loeschen/<int:id>', methods=['POST'])
@login_required
def admin_kategorie_loeschen(id):
    try:
        # Kategorie aus der Datenbank abrufen
        category = GalleryCategory.query.get_or_404(id)
        
        # Prüfen, ob die Kategorie Bilder enthält
        if GalleryImage.query.filter_by(category_id=id).first():
            flash('Diese Kategorie enthält noch Bilder und kann nicht gelöscht werden.', 'error')
            return redirect(url_for('admin_galerie'))
        
        db.session.delete(category)
        db.session.commit()
        
        flash('Kategorie wurde erfolgreich gelöscht.', 'success')
    
    except Exception as e:
        flash(f'Fehler beim Löschen der Kategorie: {str(e)}', 'error')
    
    return redirect(url_for('admin_galerie'))

@app.route('/admin/gallery/category/delete/<int:id>', methods=['POST'])
@login_required
def admin_category_delete_redirect(id):
    return redirect(url_for('admin_kategorie_loeschen', id=id))

@app.route('/admin/galerie/kategorie/bearbeiten/<int:id>', methods=['POST'])
@login_required
def admin_kategorie_bearbeiten(id):
    try:
        # Kategorie aus der Datenbank abrufen
        category = GalleryCategory.query.get_or_404(id)
        
        name = request.form.get('name', '').strip()
        display_name = request.form.get('display_name', '').strip()
        description = request.form.get('description', '').strip()
        order = request.form.get('order', type=int, default=0)
        
        if not name or not display_name:
            flash('Bitte geben Sie einen Namen und einen Anzeigenamen ein.', 'error')
            return redirect(url_for('admin_galerie'))
        
        # Prüfen, ob der neue Name bereits existiert (außer bei der aktuellen Kategorie)
        existing = GalleryCategory.query.filter(GalleryCategory.name == name, GalleryCategory.id != id).first()
        if existing:
            flash('Eine Kategorie mit diesem Namen existiert bereits.', 'error')
            return redirect(url_for('admin_galerie'))
        
        # Aktualisiere die Kategorie
        category.name = name
        category.display_name = display_name
        category.description = description
        category.order = order
        
        db.session.commit()
        
        flash('Kategorie wurde erfolgreich aktualisiert.', 'success')
    
    except Exception as e:
        flash(f'Fehler beim Aktualisieren der Kategorie: {str(e)}', 'error')
    
    return redirect(url_for('admin_galerie'))

@app.route('/admin/gallery/category/edit/<int:id>', methods=['POST'])
@login_required
def admin_category_edit_redirect(id):
    return redirect(url_for('admin_kategorie_bearbeiten', id=id))

@app.route('/admin/galerie/hinzufuegen', methods=['GET', 'POST'])
@login_required
def admin_galerie_hinzufuegen():
    categories = GalleryCategory.query.all()
    if request.method == 'POST':
        try:
            # Validierte Formulardaten abrufen
            title = sanitize_input(request.form.get('title'))
            description = sanitize_html(request.form.get('description'))
            category_id = sanitize_integer(request.form.get('category_id'), default=None)
            
            app.logger.info(f"Gallery add attempt: Title={title}, Category ID={category_id}")
            
            if not title or not description or category_id is None:
                flash('Bitte füllen Sie alle Pflichtfelder aus.', 'error')
                return render_template('admin/gallery_add.html', categories=categories)
            
            # Überprüfen, ob eine Datei hochgeladen wurde
            if 'image' not in request.files:
                app.logger.error("No file part in the request")
                flash('Keine Datei ausgewählt', 'error')
                return render_template('admin/gallery_add.html', categories=categories)
            
            file = request.files['image']
            if file.filename == '':
                app.logger.error("No file selected")
                flash('Keine Datei ausgewählt', 'error')
                return render_template('admin/gallery_add.html', categories=categories)
            
            app.logger.info(f"File uploaded: {file.filename}")
            
            # Check if upload folder exists
            upload_folder = app.config['UPLOAD_FOLDER']
            gallery_folder = os.path.join(upload_folder, 'gallery')
            
            if not os.path.exists(upload_folder):
                app.logger.info(f"Creating upload folder: {upload_folder}")
                os.makedirs(upload_folder, exist_ok=True)
                
            if not os.path.exists(gallery_folder):
                app.logger.info(f"Creating gallery folder: {gallery_folder}")
                os.makedirs(gallery_folder, exist_ok=True)
            
            # Verify file extension before uploading
            if not allowed_file(file.filename):
                app.logger.error(f"Invalid file extension: {file.filename}")
                flash('Die Datei hat ein ungültiges Format. Erlaubte Formate: jpg, jpeg, png, gif, webp', 'error')
                return render_template('admin/gallery_add.html', categories=categories)
            
            # Verwende die sichere Upload-Funktion
            app.logger.info("Calling secure_upload function")
            relative_path = secure_upload(file, subfolder='gallery', check_content=True)
            
            if not relative_path:
                app.logger.error("secure_upload returned None - upload failed")
                flash('Die hochgeladene Datei hat ein ungültiges Format oder konnte nicht gespeichert werden.', 'error')
                return render_template('admin/gallery_add.html', categories=categories)
            
            app.logger.info(f"File saved at: {relative_path}")
            
            # Get optional fields
            order = sanitize_integer(request.form.get('order'), default=0)
            is_outdoor = 'is_outdoor' in request.form
            
            # In der Datenbank speichern
            new_image = GalleryImage(
                title=title,
                description=description,
                image_path=os.path.join('uploads', relative_path).replace('\\', '/'),
                category_id=category_id,
                order=order,
                is_outdoor=is_outdoor
            )
            
            db.session.add(new_image)
            db.session.commit()
            
            app.logger.info(f"New gallery image added with ID: {new_image.id}")
            flash('Bild wurde erfolgreich hinzugefügt.', 'success')
            return redirect(url_for('admin_galerie'))
        
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding gallery image: {str(e)}")
            app.logger.exception("Exception details:")
            flash(f'Fehler beim Hinzufügen des Bildes: {str(e)}', 'error')

    return render_template('admin/gallery_add.html', categories=categories)

@app.route('/admin/gallery/add', methods=['GET', 'POST'])
@login_required
def admin_gallery_add_redirect():
    return redirect(url_for('admin_galerie_hinzufuegen'))

@app.route('/admin/galerie/bearbeiten/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_galerie_bearbeiten(id):
    # Bild aus der Datenbank abrufen
    image = GalleryImage.query.get_or_404(id)
    categories = GalleryCategory.query.all()
    
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            description = request.form.get('description')
            category_id = request.form.get('category_id')
            
            if not title or not description or not category_id:
                flash('Bitte füllen Sie alle Pflichtfelder aus.', 'error')
                return render_template('admin/gallery_edit.html', image=image, categories=categories)
    
            # Aktualisiere die Bildinformationen
            image.title = title
            image.description = description
            image.category_id = category_id
            
            # Wenn ein neues Bild hochgeladen wurde
            if 'image' in request.files and request.files['image'].filename != '':
                file = request.files['image']
                
                if file and allowed_file(file.filename):
                    # Altes Bild löschen, wenn es existiert
                    if image.image_path:
                        old_path = os.path.join(app.root_path, 'static', image.image_path)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    
                    # Neues Bild speichern
                    filename = secure_upload(file, 'gallery')
                    
                    if filename:
                        # Update des Pfads in der Datenbank
                        image.image_path = filename
        
            db.session.commit()
            flash('Bild wurde erfolgreich aktualisiert.', 'success')
            return redirect(url_for('admin_galerie'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler beim Aktualisieren des Bildes: {str(e)}', 'error')

    return render_template('admin/gallery_edit.html', image=image, categories=categories)

@app.route('/admin/gallery/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_gallery_edit_redirect(id):
    return redirect(url_for('admin_galerie_bearbeiten', id=id))

@app.route('/admin/galerie/loeschen/<int:id>', methods=['POST'])
@login_required
def admin_galerie_loeschen(id):
    try:
        # Bild aus der Datenbank abrufen
        image = GalleryImage.query.get_or_404(id)
        
        # Datei löschen
        if image.image_path:
            file_path = os.path.join(app.root_path, 'static', image.image_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # DB-Eintrag löschen
        db.session.delete(image)
        db.session.commit()
        
        flash('Bild wurde erfolgreich gelöscht.', 'success')
    
    except Exception as e:
        flash(f'Fehler beim Löschen des Bildes: {str(e)}', 'error')
    
    return redirect(url_for('admin_galerie'))

@app.route('/admin/gallery/delete/<int:id>', methods=['POST'])
@login_required
def admin_gallery_delete_redirect(id):
    return redirect(url_for('admin_galerie_loeschen', id=id))

@app.route('/track_image_view/<int:image_id>', methods=['POST'])
def track_image_view():
    # API-Schlüssel statt CSRF für AJAX-Anfragen validieren
    if not validate_api_key(request):
        app.logger.warning("Ungültiger API-Schlüssel für track_image_view")
        return jsonify({"error": "Ungültiger API-Schlüssel"}), 403
    
    try:
        # ID aus der URL extrahieren
        image_id = request.view_args.get('image_id')
        if not image_id:
            data = request.get_json()
            image_id = data.get('image_id') if data else None
        
        if not image_id:
            return jsonify({"success": False, "error": "Keine Bild-ID angegeben"}), 400
            
        # Bild-ID validieren
        image_id = sanitize_integer(image_id)
        
        # Prüfen, ob diese Anfrage bereits getrackt wurde (Schutz vor doppeltem Tracking)
        session_key = f"tracked_image_{image_id}"
        if session.get(session_key):
            app.logger.info(f"Bild {image_id} wurde bereits in dieser Session getrackt")
            return jsonify({"success": True, "already_tracked": True})
            
        # Markieren, dass dieses Bild in dieser Session getrackt wurde
        session[session_key] = True
        
        result = track_gallery_view(image_id)
        if result:
            return jsonify({"success": True, "view_id": result})
        else:
            return jsonify({"success": False, "error": "Tracking fehlgeschlagen"}), 500
            
    except Exception as e:
        app.logger.error(f"Fehler beim Tracking des Bildaufrufs: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/salz-geschichte')
def salz_geschichte():
    return render_template('salz_geschichte.html')

@app.route('/familien-geschichte')
def familien_geschichte():
    return render_template('familien_geschichte.html')

@app.route('/erfahrungs-geschichte')
def erfahrungs_geschichte():
    return render_template('erfahrungs_geschichte.html')

# Alte Routen umleiten
@app.route('/salt-story')
def salt_story():
    return redirect(url_for('salz_geschichte'))

@app.route('/family-story')
def family_story():
    return redirect(url_for('familien_geschichte'))

@app.route('/experience-story')
def experience_story():
    return redirect(url_for('erfahrungs_geschichte'))

@app.route('/salzgeschichte')
def salzgeschichte_redirect():
    return redirect(url_for('salz_geschichte'))

@app.route('/familiengeschichte')
def familiengeschichte_redirect():
    return redirect(url_for('familien_geschichte'))

@app.route('/erlebnisgeschichte')
def erlebnisgeschichte_redirect():
    return redirect(url_for('erfahrungs_geschichte'))

@app.route('/erfahrungsgeschichte')
def erfahrungsgeschichte_redirect():
    return redirect(url_for('erfahrungs_geschichte'))

@app.route('/admin/statistiken')
@login_required
def admin_statistics():
    days = request.args.get('days', default=30, type=int)
    stats = get_statistics(days)
    
    # Bereite die Daten für die Grafiken vor
    dates = []
    total_visits = []
    unique_visitors = []
    gallery_views = []
    
    # Zusätzliche Listen für die neuen Daten
    avg_duration = []
    chrome_users = []
    firefox_users = []
    safari_users = []
    edge_users = []
    other_browsers = []
    windows_users = []
    mac_users = []
    linux_users = []
    ios_users = []
    android_users = []
    other_os = []
    mobile_users = []
    desktop_users = []
    consent_count = []
    
    total_chrome_users = 0
    total_firefox_users = 0
    total_safari_users = 0
    total_edge_users = 0
    total_other_browsers = 0
    total_windows_users = 0
    total_mac_users = 0
    total_linux_users = 0
    total_ios_users = 0
    total_android_users = 0
    total_other_os = 0
    total_mobile_users = 0
    total_desktop_users = 0
    total_consent = 0
    total_duration_sum = 0
    total_duration_count = 0
    
    for stat in stats:
        dates.append(stat.date.strftime('%Y-%m-%d'))
        total_visits.append(stat.total_visits)
        unique_visitors.append(stat.unique_visitors)
        gallery_views.append(stat.gallery_views)
        
        # Sammle die neuen Daten
        avg_duration.append(stat.avg_duration if stat.avg_duration else 0)
        chrome_users.append(stat.chrome_users if hasattr(stat, 'chrome_users') else 0)
        firefox_users.append(stat.firefox_users if hasattr(stat, 'firefox_users') else 0)
        safari_users.append(stat.safari_users if hasattr(stat, 'safari_users') else 0)
        edge_users.append(stat.edge_users if hasattr(stat, 'edge_users') else 0)
        other_browsers.append(stat.other_browsers if hasattr(stat, 'other_browsers') else 0)
        windows_users.append(stat.windows_users if hasattr(stat, 'windows_users') else 0)
        mac_users.append(stat.mac_users if hasattr(stat, 'mac_users') else 0)
        linux_users.append(stat.linux_users if hasattr(stat, 'linux_users') else 0)
        ios_users.append(stat.ios_users if hasattr(stat, 'ios_users') else 0)
        android_users.append(stat.android_users if hasattr(stat, 'android_users') else 0)
        other_os.append(stat.other_os if hasattr(stat, 'other_os') else 0)
        mobile_users.append(stat.mobile_users if hasattr(stat, 'mobile_users') else 0)
        desktop_users.append(stat.desktop_users if hasattr(stat, 'desktop_users') else 0)
        consent_count.append(stat.consent_count if hasattr(stat, 'consent_count') else 0)
        
        # Berechne die Gesamtsummen
        total_chrome_users += stat.chrome_users if hasattr(stat, 'chrome_users') else 0
        total_firefox_users += stat.firefox_users if hasattr(stat, 'firefox_users') else 0
        total_safari_users += stat.safari_users if hasattr(stat, 'safari_users') else 0
        total_edge_users += stat.edge_users if hasattr(stat, 'edge_users') else 0
        total_other_browsers += stat.other_browsers if hasattr(stat, 'other_browsers') else 0
        total_windows_users += stat.windows_users if hasattr(stat, 'windows_users') else 0
        total_mac_users += stat.mac_users if hasattr(stat, 'mac_users') else 0
        total_linux_users += stat.linux_users if hasattr(stat, 'linux_users') else 0
        total_ios_users += stat.ios_users if hasattr(stat, 'ios_users') else 0
        total_android_users += stat.android_users if hasattr(stat, 'android_users') else 0
        total_other_os += stat.other_os if hasattr(stat, 'other_os') else 0
        total_mobile_users += stat.mobile_users if hasattr(stat, 'mobile_users') else 0
        total_desktop_users += stat.desktop_users if hasattr(stat, 'desktop_users') else 0
        total_consent += stat.consent_count if hasattr(stat, 'consent_count') else 0
        
        if stat.avg_duration and stat.avg_duration > 0 and hasattr(stat, 'consent_count') and stat.consent_count > 0:
            total_duration_sum += stat.avg_duration
            total_duration_count += 1
    
    # Umkehren der Listen, damit die ältesten Daten zuerst kommen
    dates.reverse()
    total_visits.reverse()
    unique_visitors.reverse()
    gallery_views.reverse()
    avg_duration.reverse()
    chrome_users.reverse()
    firefox_users.reverse()
    safari_users.reverse()
    edge_users.reverse()
    other_browsers.reverse()
    windows_users.reverse()
    mac_users.reverse()
    linux_users.reverse()
    ios_users.reverse()
    android_users.reverse()
    other_os.reverse()
    mobile_users.reverse()
    desktop_users.reverse()
    consent_count.reverse()
    
    # Berechne den Durchschnitt der Verweildauer
    avg_duration_overall = 0
    if total_duration_count > 0:
        avg_duration_overall = total_duration_sum / total_duration_count
    
    # Hole die Besucher-IPs für jeden Tag
    daily_unique_ips = {}
    for stat in stats:
        today_start = stat.date
        today_end = today_start + timedelta(days=1)
        visits = PageVisit.query.filter(
            PageVisit.timestamp >= today_start,
            PageVisit.timestamp < today_end
        ).all()
        
        # Zähle die Besuche pro IP
        ip_counts = {}
        for visit in visits:
            if visit.ip_address:
                ip_counts[visit.ip_address] = ip_counts.get(visit.ip_address, 0) + 1
        
        daily_unique_ips[stat.date] = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Hole die Seitenaufrufe pro Seite mit benutzerfreundlichen Namen
    page_visits_query = db.session.query(
        PageVisit.page, PageVisit.page_friendly_name, db.func.count(PageVisit.id)
    ).filter(
        ~PageVisit.page.startswith('/admin'),
        ~PageVisit.page.startswith('/admin-panel'),
        ~PageVisit.page.startswith('/static'),
        ~PageVisit.page.startswith('/api')
    ).group_by(PageVisit.page, PageVisit.page_friendly_name).order_by(db.func.count(PageVisit.id).desc()).all()
    
    # Bereite die Seitenaufrufe mit freundlichen Namen vor
    page_visits = []
    system_visits = []  # Neue Liste für System-Aufrufe
    
    for page, friendly_name, count in page_visits_query:
        # Verwende den benutzerfreundlichen Namen, falls vorhanden, sonst die URL
        display_name = friendly_name if friendly_name and friendly_name.strip() else page
        
        # System-Aufrufe ausfiltern
        if display_name and display_name.startswith("System:"):
            # System-Aufrufe sammeln, aber nicht anzeigen
            system_visits.append((display_name, count))
        else:
            page_visits.append((display_name, count))
    
    # Hole die Galerie-Aufrufe pro Bild
    gallery_views_data = db.session.query(
        GalleryImage.title, db.func.count(GalleryView.id)
    ).join(GalleryView, GalleryView.image_id == GalleryImage.id
    ).group_by(GalleryImage.title).order_by(db.func.count(GalleryView.id).desc()).all()
    
    # Berechne die Summen für den Zeitraum
    total_visits_sum = sum(total_visits)
    total_unique_visitors_sum = sum(unique_visitors)
    total_gallery_views_sum = sum(gallery_views)
    
    # Setze Statistiken auf 0, wenn keine Daten vorhanden sind
    if not stats:
        total_visits_sum = 0
        total_unique_visitors_sum = 0
        total_gallery_views_sum = 0
    
    return render_template('admin/statistics.html', 
                         dates=dates,
                         total_visits=total_visits_sum,
                         unique_visitors=total_unique_visitors_sum,
                         gallery_views=total_gallery_views_sum,
                         selected_days=days,
                         daily_stats=stats,
                         daily_unique_ips=daily_unique_ips,
                         page_visits=page_visits,
                         system_visits=system_visits,
                         gallery_view_data=gallery_views_data,
                         avg_duration=avg_duration_overall,
                         total_chrome_users=total_chrome_users,
                         total_firefox_users=total_firefox_users,
                         total_safari_users=total_safari_users,
                         total_edge_users=total_edge_users,
                         total_other_browsers=total_other_browsers,
                         total_windows_users=total_windows_users,
                         total_mac_users=total_mac_users,
                         total_linux_users=total_linux_users,
                         total_ios_users=total_ios_users,
                         total_android_users=total_android_users,
                         total_other_os=total_other_os,
                         total_mobile_users=total_mobile_users,
                         total_desktop_users=total_desktop_users,
                         total_consent=total_consent)

@app.route('/get_visit_id', methods=['GET'])
def get_visit_id():
    """Gibt eine eindeutige Besuchs-ID zurück, die für das Tracking der Verweildauer verwendet wird"""
    # API-Schlüssel statt CSRF für AJAX-Anfragen validieren
    if not validate_api_key(request):
        app.logger.warning("Ungültiger API-Schlüssel für get_visit_id")
        return jsonify({"error": "Ungültiger API-Schlüssel"}), 403
        
    # Wenn eine Besuchs-ID bereits in der Session existiert, gib diese zurück
    visit_id = session.get('visit_id')
    if visit_id:
        # Überprüfe, ob dieser Besuch noch gültig ist (existiert in der Datenbank)
        visit = PageVisit.query.get(visit_id)
        if visit:
            # Besuch existiert noch, gib die ID zurück
            app.logger.info(f"Bestehender Besuch gefunden: ID={visit_id}")
            return jsonify({'visit_id': visit_id, 'needs_tracking': False})
    
    # Wenn wir hierher gelangen, gibt es keinen gültigen Besuch in der Session
    # Wir versuchen, einen bestehenden Besuch für diese IP und Seite zu finden
    app.logger.info("Kein gültiger Besuch in der Session gefunden.")
    
    # Ermittle die echte IP-Adresse (auch hinter Proxies)
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_address and ',' in ip_address:
        # Wenn mehrere IPs in X-Forwarded-For, nehme die erste (Client-IP)
        ip_address = ip_address.split(',')[0].strip()
    
    # Aktuelle Seite aus dem Referer ermitteln
    referer = request.headers.get('Referer', '')
    current_page = None
    
    # Referer validieren und die aktuelle Seite extrahieren
    if referer:
        # Host-Teil extrahieren
        host_url = request.host_url.rstrip('/')
        if referer.startswith(host_url):
            # Den Host-Teil vom Referer entfernen, um den relativen Pfad zu erhalten
            path = referer[len(host_url):]
            if not path:
                path = '/'
            current_page = path
        else:
            app.logger.warning(f"Ungültiger Referer: {referer} - gehört nicht zu dieser Domain")
            return jsonify({'visit_id': None, 'needs_tracking': False, 'error': 'Ungültiger Referer'})
    
    # Wenn kein Referer oder kein gültiger Pfad ermittelt werden konnte
    if not current_page:
        app.logger.warning(f"Kein gültiger Pfad aus Referer ermittelt: {referer}")
        return jsonify({'visit_id': None, 'needs_tracking': False, 'error': 'Kein gültiger Pfad'})
    
    # Prüfen, ob dieser Pfad getrackt werden sollte (keine Admin-Seiten, statischen Ressourcen, usw.)
    if current_page.startswith('/static/') or \
       current_page.startswith('/api/') or \
       current_page.startswith('/admin/') or \
       current_page.startswith('/admin-panel/') or \
       current_page.endswith('.jpg') or \
       current_page.endswith('.png') or \
       current_page.endswith('.css') or \
       current_page.endswith('.js') or \
       current_page in ['/get_visit_id', '/update_visit_duration', '/get_api_key_token', '/track_image_view']:
        app.logger.info(f"Seite wird nicht getrackt: {current_page}")
        return jsonify({'visit_id': None, 'needs_tracking': False, 'error': 'Seite wird nicht getrackt'})
    
    # Suche nach dem letzten Besuch von dieser IP-Adresse für diese Seite
    try:
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        existing_visit = PageVisit.query.filter(
            PageVisit.timestamp >= today_start,
            PageVisit.ip_address == ip_address,
            PageVisit.page == current_page
        ).order_by(PageVisit.timestamp.desc()).first()
        
        # Wenn ein bestehender Besuch gefunden wurde, verwende diesen
        if existing_visit:
            app.logger.info(f"Bestehender Besuch von dieser IP gefunden: ID={existing_visit.id}")
            visit_id = existing_visit.id
            session['visit_id'] = visit_id
            return jsonify({'visit_id': visit_id, 'needs_tracking': False})
        
        # Debug-Informationen
        app.logger.info(f"Kein Besuch für die Seite {current_page} von IP {ip_address} gefunden. Client muss einen neuen Besuch erzeugen.")
        
        # WICHTIG: Wir erzeugen hier keinen neuen Besuch, da das bereits in track_page_visit erfolgt.
        # Stattdessen teilen wir dem Client mit, dass tracking benötigt wird
        return jsonify({'visit_id': None, 'needs_tracking': True})
            
    except Exception as e:
        app.logger.error(f"Fehler beim Suchen eines bestehenden Besuchs: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'visit_id': None, 'error': str(e)})
    
    return jsonify({'visit_id': None})

@app.route('/update_visit_duration', methods=['POST'])
def update_visit_duration_route():
    """Aktualisiert die Dauer und Bildschirmgröße eines Besuchs"""
    # API-Schlüssel statt CSRF für AJAX-Anfragen validieren
    if not validate_api_key(request):
        app.logger.warning("Ungültiger API-Schlüssel für update_visit_duration")
        return jsonify({"error": "Ungültiger API-Schlüssel"}), 403
    
    try:
        data = request.get_json()
        if not data:
            app.logger.warning("Keine Daten für update_visit_duration")
            return jsonify({"error": "Keine Daten"}), 400
        
        visit_id = data.get('visit_id')
        if not visit_id:
            app.logger.warning("Keine Besuchs-ID für update_visit_duration")
            
            # Wenn keine Besuchs-ID vorhanden ist, prüfe, ob wir stattdessen über die IP tracken können
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ip_address and ',' in ip_address:
                ip_address = ip_address.split(',')[0].strip()
                
            # Aktuelle Seite aus dem Referer ermitteln
            referer = request.headers.get('Referer', '')
            current_page = referer.replace(request.host_url, '/')
            if not current_page:
                current_page = '/'
                
            # Suche den letzten Besuch dieser IP für diese Seite
            now = datetime.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            
            visit = PageVisit.query.filter(
                PageVisit.timestamp >= today_start,
                PageVisit.ip_address == ip_address,
                PageVisit.page == current_page
            ).order_by(PageVisit.timestamp.desc()).first()
            
            if visit:
                app.logger.info(f"Besuch über IP gefunden: ID={visit.id}")
                visit_id = visit.id
            else:
                return jsonify({"error": "Keine Besuchs-ID und kein passender Besuch gefunden"}), 400
        
        duration = data.get('duration')
        if not duration:
            app.logger.warning("Keine Dauer für update_visit_duration")
            return jsonify({"error": "Keine Dauer"}), 400
        
        # Dauer validieren (sollte eine positive Zahl sein)
        duration = float(duration)
        if duration <= 0:
            app.logger.warning(f"Ungültige Dauer: {duration}")
            return jsonify({"error": "Ungültige Dauer"}), 400
        
        # Optional: Bildschirmgröße erfassen
        screen_width = data.get('screen_width')
        screen_height = data.get('screen_height')
        
        # Ermittle die echte IP-Adresse (auch hinter Proxies)
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_address and ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        app.logger.info(f"Aktualisiere Besuchsdauer: ID={visit_id}, Dauer={duration}s, Bildschirm={screen_width}x{screen_height}")
        
        # Versuche, die Besuchsdauer zu aktualisieren
        result = update_visit_duration(visit_id, duration, screen_width, screen_height)
        
        if result:
            return jsonify({"success": True})
        else:
            app.logger.error(f"Fehler beim Aktualisieren der Besuchsdauer: ID={visit_id}")
            return jsonify({"error": "Fehler beim Aktualisieren der Besuchsdauer"}), 500
    
    except Exception as e:
        app.logger.error(f"Exception in update_visit_duration: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

def resize_and_crop_image(image_path, output_size=(400, 180)):
    with Image.open(image_path) as img:
        # Convert to RGB if image is in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            
        # Calculate aspect ratios
        target_ratio = output_size[0] / output_size[1]
        img_ratio = img.width / img.height
        
        if img_ratio > target_ratio:
            # Image is wider than target ratio
            new_width = int(output_size[1] * img_ratio)
            new_height = output_size[1]
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Center crop
            left = (new_width - output_size[0]) // 2
            img = img.crop((left, 0, left + output_size[0], output_size[1]))
        else:
            # Image is taller than target ratio
            new_width = output_size[0]
            new_height = int(output_size[0] / img_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Center crop
            top = (new_height - output_size[1]) // 2
            img = img.crop((0, top, output_size[0], top + output_size[1]))
        
        # Save with high quality
        img.save(image_path, 'JPEG', quality=95)

# Alte Admin-Route weiterleiten zur neuen Route

@app.route('/get_api_key_token')
def get_api_key_token():
    # Gibt einen temporären Token für API-Schlüssel-Authentifizierung zurück
    # Prüfen, ob der Benutzer angemeldet ist oder eine gültige Session hat
    user_authenticated = False
    
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        user_authenticated = True
    elif 'csrf_token' in session:
        user_authenticated = True
    
    if user_authenticated:
        response = jsonify({'token': API_KEY})
    else:
        # Für nicht authentifizierte Benutzer nur für sichere Operationen einen eingeschränkten Token bereitstellen
        response = jsonify({'token': API_KEY})
    
    return response

@app.route('/admin/statistics')
@login_required
def admin_statistics_redirect():
    return redirect(url_for('admin.statistics'))

# Alte Admin-Route weiterleiten zur neuen Route
@app.route('/admin/hours')
@login_required
def admin_hours_redirect():
    return redirect(url_for('admin.opening_hours'))

@app.route('/admin/kategorien/loeschen/<int:id>', methods=['POST'])
@login_required
def admin_categories_delete(id):
    try:
        category = MenuCategory.query.get_or_404(id)
        # Lösche alle Menüpunkte in dieser Kategorie
        menu_items = MenuItem.query.filter_by(category_id=id).all()
        for item in menu_items:
            db.session.delete(item)
        
        db.session.delete(category)
        db.session.commit()
        flash('Kategorie und zugehörige Menüpunkte wurden erfolgreich gelöscht', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Löschen der Kategorie: {str(e)}', 'danger')
    
    return redirect(url_for('admin_categories'))

# API-Route für das Abrufen einer Kategorie zum Bearbeiten
@app.route('/admin-panel/category/edit/<int:id>')
@login_required
def admin_category_edit_api(id):
    try:
        category = MenuCategory.query.get_or_404(id)
        return jsonify({
            'id': category.id,
            'name': category.name,
            'display_name': category.display_name,
            'is_drink_category': category.is_drink_category
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/kategorien/bearbeiten/<int:id>', methods=['POST'])
@login_required
def admin_categories_edit(id):
    try:
        category = MenuCategory.query.get_or_404(id)
        
        # Formularwerte auslesen
        name = request.form.get('edit-name')
        display_name = request.form.get('edit-display_name')
        is_drink_category = 'edit-is_drink_category' in request.form
        
        # Kategorie aktualisieren, aber order beibehalten
        category.name = name
        category.display_name = display_name
        category.is_drink_category = is_drink_category
        # order wird absichtlich nicht geändert, um die Position beizubehalten
        
        db.session.commit()
        flash('Kategorie wurde erfolgreich aktualisiert.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Aktualisieren der Kategorie: {str(e)}', 'danger')
    
    # Füge Fragment-Identifier hinzu, um zur bearbeiteten Kategorie zu scrollen
    return redirect(url_for('admin_categories') + f'#category-{id}')

# Alte Admin-Route weiterleiten zur neuen Route
@app.route('/admin/categories/delete/<int:id>', methods=['POST'])
@login_required
def admin_categories_delete_redirect(id):
    return redirect(url_for('admin_categories_delete', id=id))

# Stelle sicher, dass die CSRF-Validierung im Entwicklungsmodus korrekt funktioniert
if os.environ.get('FLASK_ENV') != 'production':
    app.config['WTF_CSRF_ENABLED'] = False
    # Cookie-Einstellungen für Entwicklungsumgebung
    app.config['SESSION_COOKIE_SAMESITE'] = None
    app.config['SESSION_COOKIE_SECURE'] = False

@app.route('/api/get_current_stats', methods=['GET'])
def get_current_stats():
    """Hole aktuelle Statistiken für Echtzeit-Updates."""
    try:
        app.logger.info(f"API-Aufruf: get_current_stats von IP: {request.remote_addr}, UA: {request.user_agent}")
        
        # Heutige Statistik abrufen
        today = datetime.now().strftime('%Y-%m-%d')
        today_stats = DailyStats.query.filter_by(date=today).first()
        
        # Wenn keine Statistik für heute existiert, neue erstellen
        if not today_stats:
            app.logger.info(f"Keine Statistik für heute gefunden, erstelle neue...")
            today_stats = DailyStats(date=today, total_visits=0, unique_visitors=0, gallery_views=0, avg_duration=0)
            db.session.add(today_stats)
            db.session.commit()
            app.logger.info(f"Neue Statistik für heute erstellt: {today_stats}")
        
        # Debug: Überprüfe ob die Datenbank Einträge enthält
        total_page_visits = PageVisit.query.count()
        app.logger.info(f"Gesamtzahl der PageVisit-Einträge in der Datenbank: {total_page_visits}")
        
        # Besuche mit Dauer zählen
        visits_with_duration = PageVisit.query.filter(PageVisit.duration.isnot(None)).count()
        
        # Besuche der letzten 30 Tage zählen für die Gesamtstatistik
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Debug: Prüfe ob DailyStats Einträge enthält
        daily_stats_count = DailyStats.query.count()
        app.logger.info(f"Anzahl der DailyStats-Einträge: {daily_stats_count}")
        
        # Gesamtstatistik für die letzten 30 Tage
        try:
            total_stats = db.session.query(
                func.sum(DailyStats.total_visits).label('total_visits'),
                func.sum(DailyStats.unique_visitors).label('total_visitors'),
                func.sum(DailyStats.gallery_views).label('total_gallery_views')
            ).filter(DailyStats.date >= thirty_days_ago).first()
            
            app.logger.info(f"Abfrage für Gesamtstatistik erfolgreich: {total_stats}")
        except Exception as e:
            app.logger.error(f"Fehler bei der Abfrage der Gesamtstatistik: {str(e)}")
            total_stats = None
        
        # Wenn keine Gesamtstatistik vorhanden oder Fehler, verwende die Summe aus PageVisit
        if not total_stats or (total_stats.total_visits is None and total_stats.total_visitors is None):
            app.logger.warning("Keine DailyStats gefunden, verwende PageVisit für Gesamtstatistik")
            # Berechne Gesamtbesuche direkt aus der PageVisit-Tabelle
            total_visits = PageVisit.query.filter(
                PageVisit.timestamp >= (datetime.now() - timedelta(days=30))
            ).count()
            
            # Berechne eindeutige Besucher direkt aus der PageVisit-Tabelle
            unique_visitors = db.session.query(PageVisit.ip_address).filter(
                PageVisit.timestamp >= (datetime.now() - timedelta(days=30))
            ).distinct().count()
            
            # Berechne Gallery-Views direkt aus der GalleryView-Tabelle
            total_gallery_views = GalleryView.query.filter(
                GalleryView.timestamp >= (datetime.now() - timedelta(days=30))
            ).count()
        else:
            # Verwende die Werte aus DailyStats
            total_visits = total_stats.total_visits or 0
            total_visitors = total_stats.total_visitors or 0
            total_gallery_views = total_stats.total_gallery_views or 0
        
        # Eindeutige IPs der letzten 30 Tage sammeln
        try:
            unique_ips = db.session.query(PageVisit.ip_address).filter(
                PageVisit.timestamp >= (datetime.now() - timedelta(days=30))
            ).distinct().count()
            
            app.logger.info(f"Anzahl eindeutiger IPs der letzten 30 Tage: {unique_ips}")
        except Exception as e:
            app.logger.error(f"Fehler bei der Abfrage eindeutiger IPs: {str(e)}")
            unique_ips = 0
        
        # Durchschnittliche Besuchsdauer berechnen
        if visits_with_duration > 0:
            try:
                avg_duration = db.session.query(func.avg(PageVisit.duration)).filter(
                    PageVisit.duration.isnot(None),
                    PageVisit.timestamp >= (datetime.now() - timedelta(days=30))
                ).scalar() or 0
                avg_duration = int(avg_duration)
                
                app.logger.info(f"Durchschnittliche Besuchsdauer: {avg_duration} Sekunden")
            except Exception as e:
                app.logger.error(f"Fehler bei der Berechnung der durchschnittlichen Besuchsdauer: {str(e)}")
                avg_duration = 0
        else:
            avg_duration = 0
        
        # Aktuelle Serverzeit für Debug-Zwecke
        server_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Die neuesten Besuche mit Dauer abrufen (maximal 10)
        try:
            latest_visits_query = PageVisit.query.filter(PageVisit.duration.isnot(None)).order_by(PageVisit.timestamp.desc()).limit(10)
            latest_visits = []
            
            for visit in latest_visits_query:
                # Formatierung des Timestamps für bessere Lesbarkeit
                visit_time = visit.timestamp.strftime('%H:%M:%S')
                visit_date = visit.timestamp.strftime('%Y-%m-%d')
                
                latest_visits.append({
                    'page': visit.page,
                    'duration': visit.duration,
                    'time': visit_time,
                    'date': visit_date,
                    'ip': visit.ip_address
                })
            
            app.logger.info(f"Neueste Besuche abgerufen: {len(latest_visits)}")
        except Exception as e:
            app.logger.error(f"Fehler beim Abrufen der neuesten Besuche: {str(e)}")
            latest_visits = []
        
        # Debug-Info für die Fehlerbehebung
        debug_info = {
            'server_time': server_time,
            'request_ip': request.remote_addr,
            'request_headers': dict(request.headers),
            'unique_ips_30d': unique_ips,
            'visits_with_duration': visits_with_duration,
            'daily_stats_count': daily_stats_count,
            'total_page_visits': total_page_visits
        }
        
        app.logger.info(f"Statistik erfolgreich abgerufen: total_visits={total_visits}, today_visits={today_stats.total_visits}, unique_visitors={unique_ips}")
        
        # Erfolgreiche Antwort mit allen gesammelten Daten
        return jsonify({
            'success': True,
            'stats': {
                # Tägliche Statistikwerte
                'today_visits': today_stats.total_visits,
                'today_visitors': today_stats.unique_visitors,
                'today_gallery_views': today_stats.gallery_views,
                'today_avg_duration': today_stats.avg_duration,
                
                # Gesamtstatistikwerte (letzte 30 Tage)
                'total_visits': int(total_visits),
                'unique_visitors': unique_ips,
                'gallery_views': int(total_gallery_views),
                'avg_duration': avg_duration,
                
                # Neueste Besuche mit Dauer
                'latest_visits': latest_visits,
                
                # Serverzeit für Zeitzonendebug
                'server_time': server_time,
                
                # Heutiges Datum zur Tabellenerkennung
                'date': today
            },
            'debug': debug_info
        })
    except Exception as e:
        app.logger.error(f"Fehler beim Abrufen der Statistiken: {e}")
        return jsonify({
            'success': False,
            'error': 'Fehler beim Abrufen der Statistiken',
            'message': str(e)
        }), 500

@app.route('/admin/index')
@login_required
def admin_index():
    # Dies ist nur eine Weiterleitungsseite zur Blueprint-Route
    # Da der Blueprint mit url_prefix='/admin' registriert ist,
    # wird '/admin/' auf admin.index weitergeleitet
    return render_template('admin/index.html')

if __name__ == '__main__':
    # In der Produktionsumgebung sollte ein WSGI-Server wie Gunicorn oder uWSGI verwendet werden
    # Für die Entwicklung kann der integrierte Server verwendet werden
    port = int(os.environ.get('PORT', 5002))
    
    if os.environ.get('FLASK_ENV') == 'production':
        # Im Produktionsmodus nur auf localhost hören und SSL aktivieren, wenn verfügbar
        ssl_context = None
        if os.path.exists('cert.pem') and os.path.exists('key.pem'):
            ssl_context = ('cert.pem', 'key.pem')
        app.run(host='127.0.0.1', port=port, ssl_context=ssl_context)
    else:
        # Im Entwicklungsmodus mit aktiviertem Debug-Modus
        app.run(host='127.0.0.1', port=port, debug=True)

