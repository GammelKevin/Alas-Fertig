from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Fleischgerichte category
    fleisch_category = MenuCategory(
        name="Fleischgerichte",
        display_name="Fleischgerichte",
        description="Alle Gerichte werden mit gemischtem Salat und hausgemachtem Dressing serviert. Alternativ Bauernsalat für einen Aufpreis von €2,50.",
        order=10,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(fleisch_category)
    db.session.commit()
    
    print(f"Category 'Fleischgerichte' created with ID: {fleisch_category.id}")
    
    # Now add all the Fleischgerichte items
    fleisch_items = [
        MenuItem(
            name="171. Sutzukakia",
            description="Gegrillte Hackfleischröllchen, mit Tomatenreis & Tzatziki.",
            price=14.9,
            category_id=fleisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="172. Gyros",
            description="Serviert mit Tomatenreis & Tzatziki.",
            price=15.9,
            category_id=fleisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="173. Souflaki",
            description="Zwei Spieße, serviert mit Tomatenreis & Tzatziki.",
            price=15.9,
            category_id=fleisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="174. Bifteki",
            description="Hacksteak gefüllt mit Schafskäse, serviert mit Tomatenreis & Tzatziki.",
            price=17.5,
            category_id=fleisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="175. Hähnchenfilet",
            description="Serviert mit Tomatenreis & Tzatziki.",
            price=15.6,
            category_id=fleisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="176. Bauernspieß",
            description="Vom Schwein mit Paprika & Zwiebeln, saftig gegrillt, dazu Folienkartoffel & Tzatziki.",
            price=20.5,
            category_id=fleisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="177. Kalbsleber",
            description="Mit gerösteten Zwiebeln, einem Hauch von Knoblauch, Kartoffelscheiben & Tzatziki.",
            price=17.5,
            category_id=fleisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="178. Rückensteak vom Grill",
            description="(Vom Schwein) mit Kräuterbutter & Tomatenreis & Tzatziki.",
            price=17.5,
            category_id=fleisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="179. Medaillons vom Grill",
            description="(Vom Schwein) mit Kräuterbutter & Tomatenreis & Tzatziki.",
            price=19.6,
            category_id=fleisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="180. Schnitzel Wiener Art",
            description="(Vom Schwein) mit Pommes Frites & Tzatziki.",
            price=16.8,
            category_id=fleisch_category.id,
            homemade=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(fleisch_items)
    db.session.commit()
    
    print(f"Added {len(fleisch_items)} menu items to 'Fleischgerichte' category")
    
print("Done!") 