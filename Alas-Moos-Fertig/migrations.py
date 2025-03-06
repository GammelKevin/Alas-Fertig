from app import app, db
from sqlalchemy import text

def migrate_db():
    with app.app_context():
        # Lösche alle existierenden Tabellen
        db.session.execute(text('DROP TABLE IF EXISTS menu_item'))
        db.session.execute(text('DROP TABLE IF EXISTS menu_category'))
        db.session.execute(text('DROP TABLE IF EXISTS opening_hours'))
        db.session.execute(text('DROP TABLE IF EXISTS user'))
        db.session.commit()
        
        # Erstelle alle Tabellen neu
        db.create_all()
        
        print("Migration erfolgreich!")

if __name__ == '__main__':
    migrate_db()
    print("Migration erfolgreich!")
