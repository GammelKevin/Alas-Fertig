from flask import Flask
from werkzeug.security import generate_password_hash
from models import User
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisiere die Datenbank
db.init_app(app)

def create_admin():
    """Erstellt einen Admin-Benutzer oder setzt das Passwort zurück"""
    with app.app_context():
        # Überprüfe, ob der Admin-Benutzer bereits existiert
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("Admin-Benutzer existiert bereits. Passwort wird zurückgesetzt.")
            admin.password_hash = generate_password_hash('admin123')
            db.session.commit()
            print("Admin-Passwort wurde zurückgesetzt auf: admin123")
        else:
            # Erstelle einen neuen Admin-Benutzer
            new_admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            
            db.session.add(new_admin)
            db.session.commit()
            print("Admin-Benutzer wurde erfolgreich erstellt!")
            
        print("Benutzername: admin")
        print("Passwort: admin123")
        print("Sie können sich jetzt im Admin-Panel anmelden.")

if __name__ == '__main__':
    create_admin()
