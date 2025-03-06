from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Gemischte Fleischplatten category
    platten_category = MenuCategory(
        name="Gemischte Fleischplatten vom Grill",
        display_name="Gemischte Fleischplatten vom Grill",
        description="Alle Gerichte werden mit gemischtem Salat und hausgemachtem Dressing serviert. Alternativ Bauernsalat für einen Aufpreis von €2,50.",
        order=11,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(platten_category)
    db.session.commit()
    
    print(f"Category 'Gemischte Fleischplatten vom Grill' created with ID: {platten_category.id}")
    
    # Now add all the Gemischte Fleischplatten items
    platten_items = [
        MenuItem(
            name="190. Mia-Platte",
            description="Gyros, Lammkotelett, Souflaki, Sutzuki mit Tomatenreis, dazu Tzatziki.",
            price=17.9,
            category_id=platten_category.id,
            homemade=True
        ),
        MenuItem(
            name="191. Alas-Platte",
            description="Souflaki, Kalbsleber, Sutzuki, Gyros mit Tomatenreis, dazu Tzatziki.",
            price=17.2,
            category_id=platten_category.id,
            homemade=True,
            recommended=True
        ),
        MenuItem(
            name="192. Meteora-Platte",
            description="Gyros, 2 St. Kalbsleber mit Tomatenreis, dazu Tzatziki.",
            price=19.9,
            category_id=platten_category.id,
            homemade=True
        ),
        MenuItem(
            name="193. Trikala-Platte",
            description="Gyros & Souflaki mit Tomatenreis, dazu Tzatziki.",
            price=17.8,
            category_id=platten_category.id,
            homemade=True
        ),
        MenuItem(
            name="194. Thessalia-Platte",
            description="Gyros & Kalamari mit Tomatenreis, dazu Tzatziki.",
            price=17.8,
            category_id=platten_category.id,
            homemade=True
        ),
        MenuItem(
            name="195. Volos-Platte",
            description="Gyros & 2 St. Sutzuki mit Tomatenreis, dazu Tzatziki.",
            price=18.2,
            category_id=platten_category.id,
            homemade=True
        ),
        MenuItem(
            name="196. Dorf-Platte",
            description="Gyros, 1 St. Souflaki & 1 St. Rückensteak mit Tomatenreis, dazu Tzatziki.",
            price=18.2,
            category_id=platten_category.id,
            homemade=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(platten_items)
    db.session.commit()
    
    print(f"Added {len(platten_items)} menu items to 'Gemischte Fleischplatten vom Grill' category")
    
print("Done!") 