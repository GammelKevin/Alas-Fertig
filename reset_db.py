from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def reset_database():
    with app.app_context():
        # Lösche alle existierenden Tabellen
        db.drop_all()
        
        # Erstelle alle Tabellen neu
        db.create_all()
        
        # Erstelle einen Admin-Benutzer
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    reset_database()
