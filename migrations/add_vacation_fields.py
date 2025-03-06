from app import db, app

def upgrade():
    with app.app_context():
        # Add new columns
        db.engine.execute('ALTER TABLE opening_hours ADD COLUMN vacation_start DATE')
        db.engine.execute('ALTER TABLE opening_hours ADD COLUMN vacation_end DATE')
        db.engine.execute('ALTER TABLE opening_hours ADD COLUMN vacation_active BOOLEAN DEFAULT FALSE')

if __name__ == '__main__':
    upgrade()
