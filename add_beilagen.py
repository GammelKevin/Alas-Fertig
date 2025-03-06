from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Beilagen category
    beilagen_category = MenuCategory(
        name="Beilagen",
        display_name="Beilagen",
        description="Verschiedene Beilagen zu unseren Hauptgerichten",
        order=16,
        is_drink_category=False
    )
    
    db.session.add(beilagen_category)
    db.session.commit()
    
    print(f"Category 'Beilagen' created with ID: {beilagen_category.id}")
    
    # Add Beilagen items
    beilagen_items = [
        MenuItem(
            name="78. Pitabrot",
            description="Traditionelles griechisches Fladenbrot",
            price=3.2,
            category_id=beilagen_category.id,
            vegetarian=True,
            vegan=True
        ),
        MenuItem(
            name="79. Butterreis",
            description="Zarter Reis mit Butter verfeinert",
            price=3.2,
            category_id=beilagen_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="80. Tomatenreis",
            description="Reis mit aromatischer Tomatensauce",
            price=4.0,
            category_id=beilagen_category.id,
            vegetarian=True,
            vegan=True
        ),
        MenuItem(
            name="81. Pommes Frites",
            description="Knusprige Pommes Frites",
            price=4.2,
            category_id=beilagen_category.id,
            vegetarian=True,
            vegan=True
        ),
        MenuItem(
            name="82. Ofenkartoffel in Folie mit Sour Cream",
            description="Im Ofen gebackene Kartoffel mit Sauerrahm",
            price=4.2,
            category_id=beilagen_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="83. Kartoffelscheiben",
            description="Gebratene Kartoffelscheiben mit Kräutern",
            price=4.2,
            category_id=beilagen_category.id,
            vegetarian=True,
            vegan=True
        )
    ]
    
    db.session.add_all(beilagen_items)
    db.session.commit()
    
    print(f"Added {len(beilagen_items)} menu items to 'Beilagen' category")
    
print("Done!") 