from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # First, let's create the Mittagsangebote category
    mittag_category = MenuCategory(
        name="Mittagsangebote",
        display_name="Mittagsangebot (Dienstag bis Freitag, 11:30–14:00 Uhr)",
        description="Zu jedem Mittagsgericht wird eine Gemüsesuppe vorweg serviert. Salat ist nicht inbegriffen.",
        order=1,
        is_drink_category=False
    )
    
    # Add the category to the database
    db.session.add(mittag_category)
    db.session.commit()
    
    print(f"Category 'Mittagsangebote' created with ID: {mittag_category.id}")
    
    # Now add all the Mittagsangebote items
    mittag_items = [
        MenuItem(
            name="500. Gyros Hausgemacht",
            description="Zartes, hausgemachtes Gyros, gewürzt nach traditioneller Art mit ausgewählten Kräutern und Gewürzen, dazu aromatischer Tomatenreis und cremiger Tzatziki.",
            price=11.7,
            category_id=mittag_category.id,
            homemade=True
        ),
        MenuItem(
            name="501. Gyros Überbacken mit Käse",
            description="Zartes, hausgemachtes Gyros in Metaxasauce, verfeinert mit einer würzigen Käsekruste und im Ofen goldbraun überbacken, dazu Kartoffelscheiben.",
            price=13.2,
            category_id=mittag_category.id,
            homemade=True
        ),
        MenuItem(
            name="502. Spaghetti me Kima",
            description="Köstliche Spaghetti, serviert mit einer herzhaften Hackfleischsauce nach griechischer Art.",
            price=9.9,
            category_id=mittag_category.id,
            homemade=True
        ),
        MenuItem(
            name="503. Soutzoukakia Smyrneika",
            description="Frisch zubereitete, würzige Hackfleischröllchen, überzogen mit einer reichhaltigen Tomatensauce, dazu servieren wir Reis.",
            price=11.9,
            category_id=mittag_category.id,
            homemade=True
        ),
        MenuItem(
            name="504. Kritharaki me Kima",
            description="Zarte griechische Nudeln, serviert mit würzigem Hackfleisch in einer aromatischen Tomatensauce.",
            price=10.9,
            category_id=mittag_category.id,
            homemade=True
        ),
        MenuItem(
            name="505. Gegrilltes Hähnchenfilet",
            description="Zart gegrilltes Hähnchenbrustfilet, begleitet von aromatischem Tomatenreis und cremigem Tzatziki.",
            price=9.8,
            category_id=mittag_category.id,
            homemade=True
        ),
        MenuItem(
            name="506. Gegrilltes Rückenfilet",
            description="Zartes Rückenfilet vom Schwein, saftig gegrillt und serviert mit knusprigen Pommes.",
            price=11.7,
            category_id=mittag_category.id,
            homemade=True
        ),
        MenuItem(
            name="507. Knuspriges Schnitzel",
            description="Knusprig paniertes Schweineschnitzel, traditionell zubereitet und serviert mit Pommes.",
            price=9.6,
            category_id=mittag_category.id,
            homemade=True
        ),
        MenuItem(
            name="508. Gemista – Gefüllte Paprika und Tomaten",
            description="Mit würzigem Reis gefüllte Paprika & Tomaten, geschmort in einer leckeren Tomatensauce.",
            price=9.7,
            category_id=mittag_category.id,
            homemade=True,
            vegetarian=True
        ),
        MenuItem(
            name="509. Dorf-Souvlaki vom Schwein",
            description="Traditionell gegrilltes Schweine-Souvlaki am Holzspieß (2 Stück), serviert mit Pommes, Tzatziki und Weißbrot.",
            price=9.9,
            category_id=mittag_category.id,
            homemade=True
        ),
        MenuItem(
            name="510. Dorf-Souvlaki vom Hähnchen",
            description="Zartes Hähnchen-Souvlaki, am Holzspieß (2 Stück) gegrillt und verfeinert mit authentischen Kräutern, serviert mit Pommes, Tzatziki und Weißbrot.",
            price=9.9,
            category_id=mittag_category.id,
            homemade=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(mittag_items)
    db.session.commit()
    
    print(f"Added {len(mittag_items)} menu items to 'Mittagsangebote' category")
    
print("Done!") 