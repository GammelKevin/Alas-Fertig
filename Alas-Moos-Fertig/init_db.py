from app import app, db, User, MenuCategory, OpeningHours
from werkzeug.security import generate_password_hash

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
                {'name': 'getraenke', 'display_name': 'Getränke', 'order': 4, 'is_drink_category': True}
            ]
            
            for cat in categories:
                category = MenuCategory(
                    name=cat['name'],
                    display_name=cat['display_name'],
                    order=cat['order'],
                    is_drink_category=cat.get('is_drink_category', False)
                )
                db.session.add(category)
        
        # Standard-Öffnungszeiten erstellen
        if not OpeningHours.query.first():
            default_hours = [
                {'day': 'Montag', 'closed': True},
                {'day': 'Dienstag', 'open_time': '11:30', 'close_time': '14:30'},
                {'day': 'Mittwoch', 'open_time': '11:30', 'close_time': '14:30'},
                {'day': 'Donnerstag', 'open_time': '11:30', 'close_time': '14:30'},
                {'day': 'Freitag', 'open_time': '11:30', 'close_time': '14:30'},
                {'day': 'Samstag', 'open_time': '17:00', 'close_time': '22:00'},
                {'day': 'Sonntag', 'open_time': '11:30', 'close_time': '14:30'}
            ]
            
            for hours in default_hours:
                opening_hours = OpeningHours(
                    day=hours['day'],
                    open_time=hours.get('open_time'),
                    close_time=hours.get('close_time'),
                    closed=hours.get('closed', False)
                )
                db.session.add(opening_hours)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
