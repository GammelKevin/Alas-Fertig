from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Suppen category
    suppen_category = MenuCategory(
        name="Suppen",
        display_name="Suppen",
        description="Traditionelle griechische Suppen",
        order=3,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(suppen_category)
    db.session.commit()
    
    print(f"Category 'Suppen' created with ID: {suppen_category.id}")
    
    # Now add all the Suppen items
    suppen_items = [
        MenuItem(
            name="16. Tirokafteri",
            description="Pikanter Schafskäsedip.",
            price=6.8,
            category_id=suppen_category.id,
            vegetarian=True,
            homemade=True
        ),
        MenuItem(
            name="17. Rote Beete-Salat",
            description="Mit Ziegenkäse & Walnüssen.",
            price=7.2,
            category_id=suppen_category.id,
            vegetarian=True,
            homemade=True
        ),
        MenuItem(
            name="18. Schafskäse",
            description="Traditioneller griechischer Schafskäse.",
            price=7.5,
            category_id=suppen_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="19. Meeresfrüchte-Salat",
            description="Hausgemacht.",
            price=13.9,
            category_id=suppen_category.id,
            homemade=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(suppen_items)
    db.session.commit()
    
    print(f"Added {len(suppen_items)} menu items to 'Suppen' category")
    
print("Done!") 