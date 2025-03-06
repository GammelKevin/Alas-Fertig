from app import app, db
from models import MenuItem
import re

# Function to remove numerical prefixes like "500." from item names
def remove_number_prefix(name):
    # This regex pattern matches numbers followed by a dot and space at the beginning of the string
    return re.sub(r'^\d+\.\s+', '', name)

# Create application context
with app.app_context():
    # Get all menu items
    menu_items = MenuItem.query.all()
    
    # Counter for changed items
    count = 0
    
    # Iterate through each item and update its name
    for item in menu_items:
        old_name = item.name
        new_name = remove_number_prefix(old_name)
        
        # Only update if the name actually changed
        if old_name != new_name:
            item.name = new_name
            count += 1
            print(f"Updated: '{old_name}' → '{new_name}'")
    
    # Commit all changes to the database
    db.session.commit()
    
    print(f"Successfully updated {count} menu items by removing numerical prefixes.")
    
print("Done!") 