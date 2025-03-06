from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Kaffee & Tee category
    kaffee_category = MenuCategory(
        name="Kaffee & Tee",
        display_name="Kaffee & Tee",
        description="Verschiedene Kaffeespezialitäten und Teesorten",
        order=13,
        is_drink_category=True
    )
    
    # Add the category to the database
    db.session.add(kaffee_category)
    db.session.commit()
    
    print(f"Category 'Kaffee & Tee' created with ID: {kaffee_category.id}")
    
    # Now add all the Kaffee & Tee items
    kaffee_items = [
        MenuItem(
            name="258. Espresso",
            description="Klassischer italienischer Espresso",
            price=3.5,
            category_id=kaffee_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="259. Espresso Doppio",
            description="Doppelter Espresso",
            price=3.5,
            category_id=kaffee_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="260. Espresso Macchiato",
            description="Espresso mit einem Hauch Milchschaum",
            price=3.5,
            category_id=kaffee_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="261. Affogato Espresso",
            description="Espresso über einer Kugel Vanilleeis",
            price=3.5,
            category_id=kaffee_category.id,
            alcohol_free=True,
            vegetarian=True
        ),
        MenuItem(
            name="262. Cappuccino",
            description="Espresso mit heißer Milch und Milchschaum",
            price=3.6,
            category_id=kaffee_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="263. Latte Macchiato",
            description="Heißer Milchkaffee mit Espresso",
            price=3.6,
            category_id=kaffee_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="264. Griechischer Mokka",
            description="Traditioneller griechischer Mokka",
            price=3.0,
            category_id=kaffee_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="265. Tasse Kaffee",
            description="Filterkaffee",
            price=0.5,
            category_id=kaffee_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="266. Tasse Tee",
            description="Verschiedene Teesorten zur Auswahl",
            price=0.5,
            category_id=kaffee_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="267. Frappe",
            description="Griechischer Eiskaffee",
            price=3.0,
            category_id=kaffee_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="268. Eis-Schokolade",
            description="Mit Vanilleeis, Schokoladensauce & Sahne.",
            price=6.7,
            category_id=kaffee_category.id,
            alcohol_free=True,
            vegetarian=True
        ),
        MenuItem(
            name="269. Eis-Kaffee",
            description="Mit Vanilleeis & Sahne.",
            price=6.7,
            category_id=kaffee_category.id,
            alcohol_free=True,
            vegetarian=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(kaffee_items)
    db.session.commit()
    
    print(f"Added {len(kaffee_items)} menu items to 'Kaffee & Tee' category")
    
print("Done!") 