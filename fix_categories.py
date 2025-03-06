from app import app, db
from models import MenuCategory, MenuItem

# Define drink category names (in German)
DRINK_CATEGORY_NAMES = [
    'Aperitifs', 
    'Kaffee & Tee', 
    'Wasser & Softdrinks', 
    'Bier', 
    'Getränke',
    'Wein',
    'Spirituosen'
]

def fix_drink_categories():
    """Fix all drink categories to make sure they have is_drink_category=True"""
    with app.app_context():
        print("Checking and fixing drink categories...")
        
        # First, print all categories for reference
        all_categories = MenuCategory.query.order_by(MenuCategory.order).all()
        print("\nCurrent categories:")
        for category in all_categories:
            print(f"{category.id}. {category.display_name} (is_drink: {category.is_drink_category})")
        
        # Fix categories based on known drink category names
        fixed_count = 0
        for category in all_categories:
            should_be_drink = any(drink_name.lower() in category.display_name.lower() for drink_name in DRINK_CATEGORY_NAMES)
            
            if should_be_drink and not category.is_drink_category:
                print(f"Fixing category: {category.display_name} (setting is_drink_category=True)")
                category.is_drink_category = True
                fixed_count += 1
        
        # Commit changes if any were made
        if fixed_count > 0:
            db.session.commit()
            print(f"Fixed {fixed_count} categories")
        else:
            print("No categories needed fixing")
        
        # Print the updated categories
        print("\nUpdated categories:")
        updated_categories = MenuCategory.query.order_by(MenuCategory.order).all()
        for category in updated_categories:
            print(f"{category.id}. {category.display_name} (is_drink: {category.is_drink_category})")

if __name__ == "__main__":
    fix_drink_categories()
    print("\nDone! Please restart the Flask application to see the changes.") 