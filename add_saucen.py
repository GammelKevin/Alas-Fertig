from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Saucen & Dips category
    saucen_category = MenuCategory(
        name="Saucen & Dips",
        display_name="Saucen & Dips",
        description="Hausgemachte Saucen und Dips zu unseren Gerichten",
        order=17,
        is_drink_category=False
    )
    
    db.session.add(saucen_category)
    db.session.commit()
    
    print(f"Category 'Saucen & Dips' created with ID: {saucen_category.id}")
    
    # Add Saucen & Dips items
    saucen_items = [
        MenuItem(
            name="207. Metaxa-Sauce",
            description="Cremige Sauce mit Metaxa-Brandy verfeinert",
            price=6.8,
            category_id=saucen_category.id,
            homemade=True,
            contains_alcohol=True
        ),
        MenuItem(
            name="208. Senf-Sauce",
            description="Hausgemachte Sauce mit feinem Senf",
            price=6.8,
            category_id=saucen_category.id,
            homemade=True,
            vegetarian=True
        ),
        MenuItem(
            name="209. Zitronen-Sauce",
            description="Frische Sauce mit Zitronenaroma",
            price=6.8,
            category_id=saucen_category.id,
            homemade=True,
            vegetarian=True
        ),
        MenuItem(
            name="210. Rahm-Sauce",
            description="Cremige Sauce aus frischer Sahne",
            price=6.8,
            category_id=saucen_category.id,
            homemade=True,
            vegetarian=True
        ),
        MenuItem(
            name="212. Ketchup",
            description="Klassischer Tomaten-Ketchup",
            price=6.8,
            category_id=saucen_category.id,
            vegetarian=True,
            vegan=True
        ),
        MenuItem(
            name="213. Mayonnaise",
            description="Klassische Mayonnaise",
            price=6.8,
            category_id=saucen_category.id,
            vegetarian=True
        )
    ]
    
    db.session.add_all(saucen_items)
    db.session.commit()
    
    print(f"Added {len(saucen_items)} menu items to 'Saucen & Dips' category")
    
print("Done!") 