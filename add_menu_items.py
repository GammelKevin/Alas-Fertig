from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    # Helper function to get category by name
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Clear existing menu items
    MenuItem.query.delete()
    db.session.commit()

    # Mittagsangebot
    mittagsangebot = [
        {
            'name': 'Gyros Hausgemacht',
            'description': 'Zartes, hausgemachtes Gyros, gewürzt nach traditioneller Art mit ausgewählten Kräutern und Gewürzen, dazu aromatischer Tomatenreis und cremiger Tzatziki.',
            'price': 11.70,
            'category': 'mittagsangebot',
            'order': 500,
            'homemade': True
        },
        {
            'name': 'Gyros Überbacken mit Käse',
            'description': 'Zartes, hausgemachtes Gyros in Metaxasauce, verfeinert mit einer würzigen Käsekruste und im Ofen goldbraun überbacken, dazu Kartoffelscheiben.',
            'price': 13.20,
            'category': 'mittagsangebot',
            'order': 501,
            'homemade': True
        },
        {
            'name': 'Spaghetti me Kima',
            'description': 'Köstliche Spaghetti, serviert mit einer herzhaften Hackfleischsauce nach griechischer Art.',
            'price': 9.90,
            'category': 'mittagsangebot',
            'order': 502
        },
        {
            'name': 'Soutzoukakia Smyrneika',
            'description': 'Frisch zubereitete, würzige Hackfleischröllchen, überzogen mit einer reichhaltigen Tomatensauce, dazu servieren wir Reis.',
            'price': 11.90,
            'category': 'mittagsangebot',
            'order': 503,
            'homemade': True
        },
        {
            'name': 'Kritharaki me Kima',
            'description': 'Zarte griechische Nudeln, serviert mit würzigem Hackfleisch in einer aromatischen Tomatensauce.',
            'price': 10.90,
            'category': 'mittagsangebot',
            'order': 504
        },
        {
            'name': 'Gegrilltes Hähnchenfilet',
            'description': 'Zart gegrilltes Hähnchenbrustfilet, begleitet von aromatischem Tomatenreis und cremigem Tzatziki.',
            'price': 9.80,
            'category': 'mittagsangebot',
            'order': 505
        },
        {
            'name': 'Gegrilltes Rückenfilet',
            'description': 'Zartes Rückenfilet vom Schwein, saftig gegrillt und serviert mit knusprigen Pommes.',
            'price': 11.70,
            'category': 'mittagsangebot',
            'order': 506
        },
        {
            'name': 'Knuspriges Schnitzel',
            'description': 'Knusprig paniertes Schweineschnitzel, traditionell zubereitet und serviert mit Pommes.',
            'price': 9.60,
            'category': 'mittagsangebot',
            'order': 507
        },
        {
            'name': 'Gemista – Gefüllte Paprika und Tomaten',
            'description': 'Mit würzigem Reis gefüllte Paprika & Tomaten, geschmort in einer leckeren Tomatensauce.',
            'price': 9.70,
            'category': 'mittagsangebot',
            'order': 508,
            'vegetarian': True
        },
        {
            'name': 'Dorf-Souvlaki vom Schwein',
            'description': 'Traditionell gegrilltes Schweine-Souvlaki am Holzspieß (2 Stück), serviert mit Pommes, Tzatziki und Weißbrot.',
            'price': 9.90,
            'category': 'mittagsangebot',
            'order': 509
        },
        {
            'name': 'Dorf-Souvlaki vom Hähnchen',
            'description': 'Zartes Hähnchen-Souvlaki, am Holzspieß (2 Stück) gegrillt und verfeinert mit authentischen Kräutern, serviert mit Pommes, Tzatziki und Weißbrot.',
            'price': 9.90,
            'category': 'mittagsangebot',
            'order': 510
        }
    ]

    # Add all menu items
    for item_data in mittagsangebot:
        category = get_category(item_data['category'])
        if category:
            item = MenuItem(
                name=item_data['name'],
                description=item_data['description'],
                price=item_data['price'],
                category_id=category.id,
                order=item_data['order'],
                vegetarian=item_data.get('vegetarian', False),
                vegan=item_data.get('vegan', False),
                homemade=item_data.get('homemade', False),
                is_lunch_special=True
            )
            db.session.add(item)

    # Commit the changes
    db.session.commit()
    print("Menu items added successfully!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
