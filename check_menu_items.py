from app import app, db
from models import MenuCategory, MenuItem

def check_menu_items():
    """Check menu items by category and identify any issues"""
    with app.app_context():
        print("Checking menu items by category...\n")
        
        # Get all categories
        categories = MenuCategory.query.order_by(MenuCategory.order).all()
        
        # Count total menu items
        total_items = MenuItem.query.count()
        print(f"Total menu items in database: {total_items}\n")
        
        # Check each category
        for category in categories:
            items = MenuItem.query.filter_by(category_id=category.id).all()
            print(f"Category: {category.display_name} (ID: {category.id}, is_drink: {category.is_drink_category})")
            print(f"Number of items: {len(items)}")
            if len(items) == 0:
                print("WARNING: This category has no menu items!")
            else:
                print("First 3 items:")
                for item in items[:3]:
                    print(f"  - {item.name} (Price: {item.price}€)")
            print("")
        
        # Check for orphaned items (items with no category or invalid category)
        orphaned_items = MenuItem.query.filter(MenuItem.category_id.notin_([c.id for c in categories])).all()
        if orphaned_items:
            print(f"\nWARNING: Found {len(orphaned_items)} orphaned items with invalid category IDs:")
            for item in orphaned_items:
                print(f"  - {item.name} (ID: {item.id}, Category ID: {item.category_id})")

if __name__ == "__main__":
    check_menu_items()
    print("Done!") 