from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Spezialitäten vom Lamm category
    lamm_category = MenuCategory(
        name="Spezialitäten vom Lamm",
        display_name="Spezialitäten vom Lamm",
        description="Alle Gerichte werden mit gemischtem Salat und hausgemachtem Dressing serviert. Alternativ Bauernsalat für einen Aufpreis von €2,50.",
        order=9,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(lamm_category)
    db.session.commit()
    
    print(f"Category 'Spezialitäten vom Lamm' created with ID: {lamm_category.id}")
    
    # Now add all the Spezialitäten vom Lamm items
    lamm_items = [
        MenuItem(
            name="154. Lammkoteletts",
            description="Mit Kartoffelscheiben, grünen Bohnen & Tzatziki.",
            price=21.6,
            category_id=lamm_category.id,
            homemade=True
        ),
        MenuItem(
            name="155. Zarte Lammhaxen aus dem Backofen",
            description="Mit Schafskäse gratiniert, dazu Kartoffelscheiben & gemischter Salat.",
            price=21.2,
            category_id=lamm_category.id,
            homemade=True
        ),
        MenuItem(
            name="156. Mit dicken Bohnen",
            description="Zartes Lammfleisch mit dicken Bohnen",
            price=17.9,
            category_id=lamm_category.id,
            homemade=True
        ),
        MenuItem(
            name="157. Mit Bamies (Okraschoten)",
            description="Zartes Lammfleisch mit traditionellen Okraschoten",
            price=17.2,
            category_id=lamm_category.id,
            homemade=True
        ),
        MenuItem(
            name="158. Mit Spaghetti",
            description="Zartes Lammfleisch mit Spaghetti",
            price=19.9,
            category_id=lamm_category.id,
            homemade=True
        ),
        MenuItem(
            name="159. Stifado",
            description="Zartes Lammfleisch mit Schalotten in Tomaten-Kräutersauce.",
            price=17.8,
            category_id=lamm_category.id,
            homemade=True
        ),
        MenuItem(
            name="160. Kleftiko",
            description="Marinierte Lammhaxe mit Schafskäse, in Alufolie gebacken, aromatisiert mit Knoblauch, Dill, Thymian, serviert mit Bratkartoffeln.",
            price=19.9,
            category_id=lamm_category.id,
            homemade=True,
            recommended=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(lamm_items)
    db.session.commit()
    
    print(f"Added {len(lamm_items)} menu items to 'Spezialitäten vom Lamm' category")
    
print("Done!") 