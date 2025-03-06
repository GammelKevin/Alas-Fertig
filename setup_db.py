from app import app, db
from models import User

def setup_database():
    with app.app_context():
        # Datenbank neu erstellen
        db.drop_all()
        db.create_all()
        
        # Admin-Benutzer erstellen
        admin = User(username='admin')
        admin.set_password('admin')
        admin.is_admin = True
        
        db.session.add(admin)
        db.session.commit()
        print("Datenbank wurde initialisiert und Admin-Benutzer wurde erstellt!")

if __name__ == '__main__':
    setup_database()
