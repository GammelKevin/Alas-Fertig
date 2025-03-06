from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Pfannengerichte category
    pfannen_category = MenuCategory(
        name="Pfannengerichte",
        display_name="Pfannengerichte",
        description="Alle Gerichte werden mit gemischtem Salat und hausgemachtem Dressing serviert. Alternativ Bauernsalat für einen Aufpreis von €2,50.",
        order=8,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(pfannen_category)
    db.session.commit()
    
    print(f"Category 'Pfannengerichte' created with ID: {pfannen_category.id}")
    
    # Now add all the Pfannengerichte items
    pfannen_items = [
        MenuItem(
            name="139. Gyros-Pfanne",
            description="In Metaxasauce zubereitet, mit Schafskäse überbacken, dazu Kartoffelscheiben.",
            price=17.5,
            category_id=pfannen_category.id,
            homemade=True
        ),
        MenuItem(
            name="140. Gyros überbacken mit Käse",
            description="In Metaxasauce zubereitet, dazu Kartoffelscheiben.",
            price=17.5,
            category_id=pfannen_category.id,
            homemade=True
        ),
        MenuItem(
            name="141. Psaronefri-Pfanne",
            description="Schweinefiletmedaillons mit Rahmsauce flambiert, dazu Kartoffelscheiben.",
            price=19.6,
            category_id=pfannen_category.id,
            homemade=True
        ),
        MenuItem(
            name="142. Musakas – Der weltbekannte Auflauf",
            description="Mit Auberginen, Hackfleisch & Kartoffeln, überbacken mit einer feinen Béchamel-Sauce.",
            price=17.9,
            category_id=pfannen_category.id,
            homemade=True
        ),
        MenuItem(
            name="143. Kotopulo-Pfanne",
            description="Hähnchenbrustfilet, überbacken in Metaxasauce, dazu Kartoffelscheiben.",
            price=17.8,
            category_id=pfannen_category.id,
            homemade=True
        ),
        MenuItem(
            name="144. Keftedakia Smyrneika – Pfanne",
            description="Frikadellen in Tomatensauce überbacken, dazu Kartoffelscheiben.",
            price=18.2,
            category_id=pfannen_category.id,
            homemade=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(pfannen_items)
    db.session.commit()
    
    print(f"Added {len(pfannen_items)} menu items to 'Pfannengerichte' category")
    
print("Done!") 