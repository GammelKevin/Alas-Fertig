from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Salate category
    salate_category = MenuCategory(
        name="Salate",
        display_name="Salate",
        description="Frische griechische Salate und Vorspeisen",
        order=4,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(salate_category)
    db.session.commit()
    
    print(f"Category 'Salate' created with ID: {salate_category.id}")
    
    # Now add all the Salate items
    salate_items = [
        MenuItem(
            name="23. Pikilia kria",
            description="Traditionelle gemischte kalte Vorspeisenplatte.",
            price=15.2,
            category_id=salate_category.id,
            homemade=True
        ),
        MenuItem(
            name="24. Dolmades",
            description="Weinblätter mit Reis (kalt).",
            price=6.7,
            category_id=salate_category.id,
            vegetarian=True,
            homemade=True
        ),
        MenuItem(
            name="25. Dolmadakia",
            description="Gefüllte Weinblätter mit Reis & Hackfleisch.",
            price=8.8,
            category_id=salate_category.id,
            homemade=True
        ),
        MenuItem(
            name="26. Zucchini-Bällchen",
            description="Hausgemachte Zucchinibällchen mit Feta, Frühlingszwiebeln & Tzatziki.",
            price=7.8,
            category_id=salate_category.id,
            vegetarian=True,
            homemade=True
        ),
        MenuItem(
            name="27. Gegrillte Peperoni",
            description="Mit Olivenöl & Balsamico.",
            price=6.4,
            category_id=salate_category.id,
            vegetarian=True,
            vegan=True
        ),
        MenuItem(
            name="28. Melitzanes / Kolokithakia",
            description="Gebratene Auberginen mit Zucchini & Tzatziki.",
            price=9.6,
            category_id=salate_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="29. Talagani",
            description="Traditioneller Grillkäse, dazu Marmelade.",
            price=9.6,
            category_id=salate_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="33. Florinis",
            description="Gegrillte rote Paprika, gefüllt mit Schafskäse.",
            price=8.6,
            category_id=salate_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="34. Feta aus dem Ofen",
            description="Mit Tomaten, Peperoni, Oliven, Knoblauch, Zwiebeln & Olivenöl.",
            price=8.9,
            category_id=salate_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="35. Feta saganaki",
            description="Schafskäse in einer goldbraunen Hülle gebraten.",
            price=8.4,
            category_id=salate_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="36. Scampi saganaki",
            description="In einer pikanten Tomatensauce mit Fetakäse überbacken.",
            price=15.2,
            category_id=salate_category.id
        ),
        MenuItem(
            name="37. Octopus vom Grill",
            description="Gegrillter Octopus mit Olivenöl und Zitrone.",
            price=16.2,
            category_id=salate_category.id
        ),
        MenuItem(
            name="38. Gavros tiganitos",
            description="Sardellen in einer goldbraunen Hülle gebraten.",
            price=10.8,
            category_id=salate_category.id
        ),
        MenuItem(
            name="39. Pikilia Zesti",
            description="Traditionelle gemischte warme Vorspeisenplatte.",
            price=16.2,
            category_id=salate_category.id,
            homemade=True
        ),
        MenuItem(
            name="40. Knoblauchbrot",
            description="Überbackenes Brot mit Knoblauch & Käse.",
            price=5.7,
            category_id=salate_category.id,
            vegetarian=True
        ),
        MenuItem(
            name="41. Calamari Krönchen",
            description="Kleine knusprig frittierte Calamari-Tentakel in goldbrauner Panade.",
            price=9.6,
            category_id=salate_category.id
        ),
        MenuItem(
            name="42. Faros",
            description="Fluffige Käsebällchen aus verschiedenen Käsesorten, goldbraun frittiert, mit würzigem Schafskäse-Paprika-Dip.",
            price=11.9,
            category_id=salate_category.id,
            vegetarian=True,
            homemade=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(salate_items)
    db.session.commit()
    
    print(f"Added {len(salate_items)} menu items to 'Salate' category")
    
print("Done!") 