from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Desserts category
    desserts_category = MenuCategory(
        name="Desserts",
        display_name="Desserts",
        description="Hausgemachte griechische und internationale Nachspeisen",
        order=12,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(desserts_category)
    db.session.commit()
    
    print(f"Category 'Desserts' created with ID: {desserts_category.id}")
    
    # Now add all the Desserts items
    desserts_items = [
        MenuItem(
            name="241. Griechischer Joghurt",
            description="Mit Honig & Walnüssen.",
            price=6.7,
            category_id=desserts_category.id,
            vegetarian=True,
            homemade=True
        ),
        MenuItem(
            name="242. Galaktoboureko",
            description="Blätterteig mit Vanilleeis-Grießcreme gefüllt & Vanilleeis.",
            price=8.3,
            category_id=desserts_category.id,
            vegetarian=True,
            homemade=True
        ),
        MenuItem(
            name="243. Mille-feuille",
            description="Blätterteig gefüllt mit Vanillecreme, Erdbeeren & Pistazien.",
            price=8.3,
            category_id=desserts_category.id,
            vegetarian=True,
            homemade=True
        ),
        MenuItem(
            name="244. Steirer-Eis",
            description="Vanilleeis mit Kürbiskernöl & karamellisierten Kürbiskernen.",
            price=6.7,
            category_id=desserts_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="245. Coupé Ananas",
            description="Vanilleeis mit frischer Ananas & Schlagsahne.",
            price=6.7,
            category_id=desserts_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="246. Heiße Feigen",
            description="Heiße Feigen gekocht in Cassis-Likör & Vanilleeis.",
            price=6.7,
            category_id=desserts_category.id,
            vegetarian=True,
            contains_alcohol=True
        ),
        MenuItem(
            name="247. Eis mit heißen Himbeeren",
            description="Vanilleeis mit heißen Himbeeren & Sahne.",
            price=6.7,
            category_id=desserts_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="248. Gemischtes Eis",
            description="Vanille-, Erdbeer- und Schokoladeneis, dazu Sahne.",
            price=6.7,
            category_id=desserts_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="249. Gadaifi",
            description="Knusprige Teigfäden mit Walnussfüllung und Zuckersirup, dazu Vanilleeis.",
            price=8.3,
            category_id=desserts_category.id,
            vegetarian=True,
            homemade=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(desserts_items)
    db.session.commit()
    
    print(f"Added {len(desserts_items)} menu items to 'Desserts' category")
    
print("Done!") 