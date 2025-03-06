from extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'))
    image_path = db.Column(db.String(255))
    vegetarian = db.Column(db.Boolean, default=False)
    vegan = db.Column(db.Boolean, default=False)
    spicy = db.Column(db.Boolean, default=False)
    gluten_free = db.Column(db.Boolean, default=False)
    lactose_free = db.Column(db.Boolean, default=False)
    kid_friendly = db.Column(db.Boolean, default=False)
    alcohol_free = db.Column(db.Boolean, default=False)
    contains_alcohol = db.Column(db.Boolean, default=False)
    homemade = db.Column(db.Boolean, default=False)
    sugar_free = db.Column(db.Boolean, default=False)
    recommended = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    category = db.relationship('MenuCategory', backref=db.backref('items', lazy=True))

class MenuCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    is_drink_category = db.Column(db.Boolean, default=False)

class OpeningHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False, unique=True)
    open_time_1 = db.Column(db.String(5))
    close_time_1 = db.Column(db.String(5))
    open_time_2 = db.Column(db.String(5))
    close_time_2 = db.Column(db.String(5))
    closed = db.Column(db.Boolean, default=False)
    vacation_start = db.Column(db.Date)
    vacation_end = db.Column(db.Date)
    vacation_active = db.Column(db.Boolean, default=False)

    def is_on_vacation(self):
        if not self.vacation_active or not self.vacation_start or not self.vacation_end:
            return False
        current_date = datetime.now().date()
        return self.vacation_start <= current_date <= self.vacation_end

    def check_vacation_expired(self):
        if self.vacation_active and self.vacation_end and self.vacation_end < datetime.now().date():
            self.vacation_active = False
            self.vacation_start = None
            self.vacation_end = None
            return True
        return False

    def validate_times(self):
        if self.closed or self.vacation_active:
            return True

        if not self.open_time_1 or not self.close_time_1:
            raise ValueError("Die erste Öffnungszeit muss vollständig angegeben werden.")

        # Zeitformat validieren (HH:MM)
        time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
        if not time_pattern.match(self.open_time_1) or not time_pattern.match(self.close_time_1):
            raise ValueError("Ungültiges Zeitformat. Bitte verwenden Sie HH:MM.")

        # Zweite Öffnungszeit validieren
        if (self.open_time_2 and not self.close_time_2) or (not self.open_time_2 and self.close_time_2):
            raise ValueError("Die zweite Öffnungszeit muss vollständig angegeben werden.")

        if self.open_time_2 and self.close_time_2:
            if not time_pattern.match(self.open_time_2) or not time_pattern.match(self.close_time_2):
                raise ValueError("Ungültiges Zeitformat. Bitte verwenden Sie HH:MM.")

        # Überprüfen, ob Schließzeit nach Öffnungszeit liegt
        if not self._is_time2_after_time1(self.open_time_1, self.close_time_1):
            raise ValueError("Die erste Schließzeit muss nach der ersten Öffnungszeit liegen.")

        if self.open_time_2 and self.close_time_2:
            if not self._is_time2_after_time1(self.open_time_2, self.close_time_2):
                raise ValueError("Die zweite Schließzeit muss nach der zweiten Öffnungszeit liegen.")
            if not self._is_time2_after_time1(self.close_time_1, self.open_time_2):
                raise ValueError("Die zweite Öffnungszeit muss nach der ersten Schließzeit liegen.")

        return True

    def _is_time2_after_time1(self, time1, time2):
        t1 = datetime.strptime(time1, '%H:%M').time()
        t2 = datetime.strptime(time2, '%H:%M').time()
        return t2 > t1

    def validate_vacation(self):
        if not self.vacation_active:
            return True

        if not self.vacation_start or not self.vacation_end:
            raise ValueError("Für den Urlaub müssen Start- und Enddatum angegeben werden.")

        if self.vacation_start > self.vacation_end:
            raise ValueError("Das Urlaubsende muss nach dem Urlaubsbeginn liegen.")

        if self.vacation_start < datetime.now().date():
            raise ValueError("Der Urlaubsbeginn darf nicht in der Vergangenheit liegen.")

        delta = self.vacation_end - self.vacation_start
        if delta.days > 365:
            raise ValueError("Der Urlaubszeitraum darf nicht länger als ein Jahr sein.")

        return True

    def to_dict(self):
        return {
            'id': self.id,
            'day': self.day,
            'vacation_active': self.vacation_active,
            'vacation_start': self.vacation_start.strftime('%Y-%m-%d') if self.vacation_start else None,
            'vacation_end': self.vacation_end.strftime('%Y-%m-%d') if self.vacation_end else None,
            'closed': self.closed,
            'open_time_1': self.open_time_1,
            'close_time_1': self.close_time_1,
            'open_time_2': self.open_time_2,
            'close_time_2': self.close_time_2
        }

    def __repr__(self):
        if self.vacation_active and self.vacation_start and self.vacation_end:
            return f"<OpeningHours {self.day} (Urlaub: {self.vacation_start} - {self.vacation_end})>"
        elif self.closed:
            return f"<OpeningHours {self.day} (Ruhetag)>"
        elif self.open_time_1 and self.close_time_1:
            times = f"{self.open_time_1}-{self.close_time_1}"
            if self.open_time_2 and self.close_time_2:
                times += f", {self.open_time_2}-{self.close_time_2}"
            return f"<OpeningHours {self.day} ({times})>"
        else:
            return f"<OpeningHours {self.day} (Keine Zeiten eingetragen)>"

class GalleryCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    images = db.relationship('GalleryImage', backref='category', lazy=True)

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_path = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('gallery_category.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_outdoor = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)

class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100), nullable=False)
    page_friendly_name = db.Column(db.String(100))  # Benutzerfreundlicher Seitenname für die Statistik
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    duration = db.Column(db.Integer)  # Verweildauer in Sekunden
    browser = db.Column(db.String(100))  # Browser-Informationen
    operating_system = db.Column(db.String(100))  # Betriebssystem
    screen_width = db.Column(db.Integer)  # Bildschirmbreite
    screen_height = db.Column(db.Integer)  # Bildschirmhöhe
    analytics_consent = db.Column(db.Boolean, default=False)  # Ob der Benutzer Analyse-Cookies akzeptiert hat

class GalleryView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('gallery_image.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))

class DailyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    total_visits = db.Column(db.Integer, nullable=False, default=0)
    unique_visitors = db.Column(db.Integer, nullable=False, default=0)
    gallery_views = db.Column(db.Integer, nullable=False, default=0)
    avg_duration = db.Column(db.Float, default=0)  # Durchschnittliche Verweildauer in Sekunden
    chrome_users = db.Column(db.Integer, default=0)  # Anzahl der Chrome-Benutzer
    firefox_users = db.Column(db.Integer, default=0)  # Anzahl der Firefox-Benutzer
    safari_users = db.Column(db.Integer, default=0)  # Anzahl der Safari-Benutzer
    edge_users = db.Column(db.Integer, default=0)  # Anzahl der Edge-Benutzer
    other_browsers = db.Column(db.Integer, default=0)  # Andere Browser
    windows_users = db.Column(db.Integer, default=0)  # Windows-Benutzer
    mac_users = db.Column(db.Integer, default=0)  # Mac-Benutzer
    linux_users = db.Column(db.Integer, default=0)  # Linux-Benutzer
    ios_users = db.Column(db.Integer, default=0)  # iOS-Benutzer
    android_users = db.Column(db.Integer, default=0)  # Android-Benutzer
    other_os = db.Column(db.Integer, default=0)  # Andere Betriebssysteme
    mobile_users = db.Column(db.Integer, default=0)  # Mobile Benutzer
    desktop_users = db.Column(db.Integer, default=0)  # Desktop-Benutzer
    consent_count = db.Column(db.Integer, default=0)  # Anzahl der Benutzer mit Analyse-Consent

    def __init__(self, date=None, total_visits=0, unique_visitors=0, gallery_views=0, 
                avg_duration=0, chrome_users=0, firefox_users=0, safari_users=0, 
                edge_users=0, other_browsers=0, windows_users=0, mac_users=0, 
                linux_users=0, ios_users=0, android_users=0, other_os=0, 
                mobile_users=0, desktop_users=0, consent_count=0):
        self.date = date
        self.total_visits = total_visits
        self.unique_visitors = unique_visitors
        self.gallery_views = gallery_views
        self.avg_duration = avg_duration
        self.chrome_users = chrome_users
        self.firefox_users = firefox_users
        self.safari_users = safari_users
        self.edge_users = edge_users
        self.other_browsers = other_browsers
        self.windows_users = windows_users
        self.mac_users = mac_users
        self.linux_users = linux_users
        self.ios_users = ios_users
        self.android_users = android_users
        self.other_os = other_os
        self.mobile_users = mobile_users
        self.desktop_users = desktop_users
        self.consent_count = consent_count
