from app import app, db, User, MenuCategory, OpeningHours, DailyStats
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def init_db():
    with app.app_context():
        db.create_all()
        
        # Admin User erstellen
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.password_hash = generate_password_hash('admin')
            db.session.add(admin)
        
        # Standard-Kategorien erstellen
        if not MenuCategory.query.first():
            categories = [
                {'name': 'vorspeisen', 'display_name': 'Vorspeisen', 'order': 1},
                {'name': 'hauptspeisen', 'display_name': 'Hauptspeisen', 'order': 2},
                {'name': 'desserts', 'display_name': 'Desserts', 'order': 3},
                {'name': 'getraenke', 'display_name': 'Getränke', 'order': 4}
            ]
            
            for cat in categories:
                category = MenuCategory(
                    name=cat['name'],
                    display_name=cat['display_name'],
                    order=cat['order']
                )
                db.session.add(category)
        
        # Standard-Öffnungszeiten erstellen
        if not OpeningHours.query.first():
            default_hours = [
                {'day': 'Montag', 'closed': True},
                {'day': 'Dienstag', 'open_time_1': '11:30', 'close_time_1': '14:30'},
                {'day': 'Mittwoch', 'open_time_1': '11:30', 'close_time_1': '14:30'},
                {'day': 'Donnerstag', 'open_time_1': '11:30', 'close_time_1': '14:30'},
                {'day': 'Freitag', 'open_time_1': '11:30', 'close_time_1': '14:30'},
                {'day': 'Samstag', 'open_time_1': '17:00', 'close_time_1': '22:00'},
                {'day': 'Sonntag', 'open_time_1': '11:30', 'close_time_1': '14:30'}
            ]
            
            for hours in default_hours:
                opening_hours = OpeningHours(
                    day=hours['day'],
                    open_time_1=hours.get('open_time_1'),
                    close_time_1=hours.get('close_time_1'),
                    closed=hours.get('closed', False)
                )
                db.session.add(opening_hours)
        
        # Beispiel-Statistiken für die letzten 30 Tage erstellen
        if not DailyStats.query.first():
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=30)
            current_date = start_date
            
            while current_date <= end_date:
                # Zufällige aber realistische Werte für die Statistiken
                stats = DailyStats(
                    date=current_date,
                    total_visits=50,  # Beispielwert
                    unique_visitors=30,  # Beispielwert
                    gallery_views=20  # Beispielwert
                )
                db.session.add(stats)
                current_date += timedelta(days=1)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
