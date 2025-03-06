from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Steak vom Grill category
    steak_category = MenuCategory(
        name="Steak vom Grill",
        display_name="Steak vom Grill",
        description="Hochwertige Steaks vom Grill",
        order=7,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(steak_category)
    db.session.commit()
    
    print(f"Category 'Steak vom Grill' created with ID: {steak_category.id}")
    
    # Now add the Steak vom Grill item
    steak_item = MenuItem(
        name="126. Rumpsteak (ca. 300 g)",
        description="Mit Kräuterbutter & Ofenkartoffel.",
        price=28.9,
        category_id=steak_category.id,
        homemade=True,
        recommended=True
    )
    
    # Add the item
    db.session.add(steak_item)
    db.session.commit()
    
    print("Added menu item to 'Steak vom Grill' category")
    
print("Done!") 