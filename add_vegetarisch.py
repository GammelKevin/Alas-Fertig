from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Vegetarische Gerichte category
    veg_category = MenuCategory(
        name="Vegetarische Gerichte",
        display_name="Vegetarische Gerichte",
        description="Alle Gerichte werden mit gemischtem Salat und hausgemachtem Dressing serviert. Alternativ Bauernsalat für einen Aufpreis von €2,50.",
        order=6,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(veg_category)
    db.session.commit()
    
    print(f"Category 'Vegetarische Gerichte' created with ID: {veg_category.id}")
    
    # Now add all the Vegetarische Gerichte items
    veg_items = [
        MenuItem(
            name="113. Stamna",
            description="Griechische Nudeln, frisches Gemüse und Kartoffeln aus dem Ofen.",
            price=7.8,
            category_id=veg_category.id,
            homemade=True,
            vegetarian=True
        ),
        MenuItem(
            name="114. Griechische Nudeln mit Gemüse & Tomatensauce",
            description="Traditionelle griechische Nudeln mit frischem Gemüse in Tomatensauce.",
            price=9.3,
            category_id=veg_category.id,
            homemade=True,
            vegetarian=True
        ),
        MenuItem(
            name="115. Gemüse Ograten",
            description="Gemüsemischung in Schlagsahne, mit Käse überbacken.",
            price=7.8,
            category_id=veg_category.id,
            homemade=True,
            vegetarian=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(veg_items)
    db.session.commit()
    
    print(f"Added {len(veg_items)} menu items to 'Vegetarische Gerichte' category")
    
print("Done!") 