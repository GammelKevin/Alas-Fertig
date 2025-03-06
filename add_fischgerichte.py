from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Fischgerichte category
    fisch_category = MenuCategory(
        name="Fischgerichte",
        display_name="Fischgerichte",
        description="Alle Gerichte werden mit gemischtem Salat und hausgemachtem Dressing serviert. Alternativ Bauernsalat für einen Aufpreis von €2,50.",
        order=5,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(fisch_category)
    db.session.commit()
    
    print(f"Category 'Fischgerichte' created with ID: {fisch_category.id}")
    
    # Now add all the Fischgerichte items
    fisch_items = [
        MenuItem(
            name="95. Baby Calamari vom Grill",
            description="Gebrillte Baby-Calamari mit Zitronen-Olivenöl, frischem Butterreis & Senfsauce.",
            price=19.2,
            category_id=fisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="96. Frittierte Baby Calamari",
            description="Panierter und frittierter Baby-Calamari mit Zitronen-Olivenöl, frischem Butterreis & Senfsauce.",
            price=19.2,
            category_id=fisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="97. Garnelen Souflaki",
            description="Gebrillte Garnelen am Spieß mit frischem Butterreis & Senfsauce.",
            price=22.6,
            category_id=fisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="98. Fischteller",
            description="Frittierte Calamari, gebrilltes Doradefilet, gebrillter Lachs, gebrillte Garnelen, frischer Butterreis, dazu Senfsauce.",
            price=24.5,
            category_id=fisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="99. Dorade Royal",
            description="Zwei Doradenfilets mit Zitronen-Olivenöl, dazu frischer Butterreis und hausgemachte Senfsauce.",
            price=24.5,
            category_id=fisch_category.id,
            homemade=True
        ),
        MenuItem(
            name="101. Lachsfilet vom Grill",
            description="Gebrilltes Lachsfilet, mit frischem Butterreis, dazu Senfsauce.",
            price=22.6,
            category_id=fisch_category.id,
            homemade=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(fisch_items)
    db.session.commit()
    
    print(f"Added {len(fisch_items)} menu items to 'Fischgerichte' category")
    
print("Done!") 