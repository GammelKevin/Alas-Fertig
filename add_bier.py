from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Bier category
    bier_category = MenuCategory(
        name="Bier",
        display_name="Bier",
        description="Verschiedene Biersorten",
        order=15,
        is_drink_category=True
    )
    
    db.session.add(bier_category)
    db.session.commit()
    
    print(f"Category 'Bier' created with ID: {bier_category.id}")
    
    # Add Bier items
    bier_items = [
        MenuItem(
            name="313. Helles vom Fass 0,3l",
            description="Frisches Helles Bier vom Fass",
            price=4.2,
            category_id=bier_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="313. Helles vom Fass 0,5l",
            description="Frisches Helles Bier vom Fass",
            price=4.5,
            category_id=bier_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="314. Dunkles 0,5l",
            description="Dunkles Bier",
            price=4.5,
            category_id=bier_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="315. Alkoholfreies Helles 0,3l",
            description="Alkoholfreies helles Bier",
            price=3.6,
            category_id=bier_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="315. Alkoholfreies Helles 0,5l",
            description="Alkoholfreies helles Bier",
            price=4.5,
            category_id=bier_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="316. Radler 0,5l",
            description="Bier mit Zitronenlimonade",
            price=4.5,
            category_id=bier_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="317. Weizen vom Fass 0,3l",
            description="Frisches Weizenbier vom Fass",
            price=3.6,
            category_id=bier_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="317. Weizen vom Fass 0,5l",
            description="Frisches Weizenbier vom Fass",
            price=4.5,
            category_id=bier_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="318. Alkoholfreies Weizen 0,5l",
            description="Alkoholfreies Weizenbier",
            price=4.5,
            category_id=bier_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="319. Cola-Weizen 0,5l",
            description="Weizenbier mit Cola",
            price=4.5,
            category_id=bier_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="320. Russen-Halbe 0,5l",
            description="Weizenbier mit Zitronenlimonade",
            price=4.5,
            category_id=bier_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="321. Pils 0,33l",
            description="Pilsner Bier",
            price=3.9,
            category_id=bier_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="322. Mytos (Griechisches Lagerbier) 0,33l",
            description="Traditionelles griechisches Lagerbier",
            price=3.9,
            category_id=bier_category.id,
            contains_alcohol=True
        )
    ]
    
    db.session.add_all(bier_items)
    db.session.commit()
    
    print(f"Added {len(bier_items)} menu items to 'Bier' category")
    
print("Done!") 