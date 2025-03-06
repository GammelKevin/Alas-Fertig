from app import app, db
from app import MenuItem

def upgrade():
    with app.app_context():
        # Add new columns
        columns = [
            'gluten_free',
            'lactose_free',
            'kid_friendly',
            'alcohol_free',
            'contains_alcohol',
            'homemade',
            'sugar_free',
            'recommended'
        ]
        
        for column in columns:
            try:
                db.session.execute(f'ALTER TABLE menu_item ADD COLUMN {column} BOOLEAN DEFAULT FALSE')
            except Exception as e:
                print(f"Column {column} might already exist: {e}")
        
        db.session.commit()

if __name__ == '__main__':
    upgrade()
