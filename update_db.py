from app import app, db
from models import OpeningHours

def update_database():
    with app.app_context():
        # Backup der alten Daten
        old_hours = OpeningHours.query.all()
        old_data = []
        for hour in old_hours:
            old_data.append({
                'day': hour.day,
                'open_time_1': hour.open_time_1,
                'close_time_1': hour.close_time_1,
                'open_time_2': hour.open_time_2,
                'close_time_2': hour.close_time_2,
                'closed': hour.closed,
                'vacation_active': hour.vacation_active,
                'vacation_start': hour.vacation_start,
                'vacation_end': hour.vacation_end
            })

        # Lösche alte Tabelle
        OpeningHours.__table__.drop(db.engine)
        db.session.commit()

        # Erstelle neue Tabelle
        OpeningHours.__table__.create(db.engine)
        db.session.commit()

        # Stelle alte Daten wieder her
        for data in old_data:
            hour = OpeningHours(**data)
            db.session.add(hour)
        
        db.session.commit()
        print("Datenbank erfolgreich aktualisiert!")

if __name__ == '__main__':
    update_database()
