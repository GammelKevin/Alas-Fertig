from app import db, app
from datetime import datetime

def upgrade():
    with app.app_context():
        try:
            # Add new columns
            db.engine.execute('ALTER TABLE opening_hours ADD COLUMN vacation_start DATE')
            print("Added vacation_start column")
            db.engine.execute('ALTER TABLE opening_hours ADD COLUMN vacation_end DATE')
            print("Added vacation_end column")
            db.engine.execute('ALTER TABLE opening_hours ADD COLUMN vacation_active BOOLEAN DEFAULT FALSE')
            print("Added vacation_active column")
            print("Migration completed successfully!")
        except Exception as e:
            print(f"Error during migration: {str(e)}")

if __name__ == '__main__':
    upgrade()
