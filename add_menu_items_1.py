from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Mittagsangebot
    mittagsangebot = [
        {'name': 'Gyros Hausgemacht', 'price': 9.60, 'category': 'mittagsangebot', 'homemade': True},
        {'name': 'Gyros Überbacken mit Käse', 'price': 10.90, 'category': 'mittagsangebot'},
        {'name': 'Spaghetti me Kima', 'price': 11.70, 'category': 'mittagsangebot'},
        {'name': 'Soutzoukakia Smyrneika', 'price': 13.20, 'category': 'mittagsangebot'},
        {'name': 'Kritharaki me Kima', 'price': 9.90, 'category': 'mittagsangebot'},
        {'name': 'Gegrilltes Hähnchenfilet', 'price': 11.70, 'category': 'mittagsangebot'},
        {'name': 'Gegrilltes Rückenfilet', 'price': 11.90, 'category': 'mittagsangebot'},
        {'name': 'Knuspriges Schnitzel', 'price': 9.80, 'category': 'mittagsangebot'},
        {'name': 'Gemista – Gefüllte Paprika und Tomaten', 'price': 9.70, 'category': 'mittagsangebot', 'vegetarian': True},
        {'name': 'Dorf-Souvlaki vom Schwein', 'price': 9.90, 'category': 'mittagsangebot'},
        {'name': 'Dorf-Souvlaki vom Hähnchen', 'price': 9.90, 'category': 'mittagsangebot'}
    ]

    # Suppen
    suppen = [
        {'name': 'Gemüsesuppe', 'description': 'vorweg serviert', 'price': 0.00, 'category': 'suppen', 'vegetarian': True}
    ]

    # Salate
    salate = [
        {'name': 'Rote Beete-Salat', 'price': 7.20, 'category': 'salate', 'vegetarian': True},
        {'name': 'Meeresfrüchte-Salat', 'price': 13.90, 'category': 'salate'}
    ]

    # Vorspeisen
    vorspeisen = [
        {'name': 'Tirokafteri', 'description': 'pikanter Schafskäsedip', 'price': 6.80, 'category': 'vorspeisen', 'vegetarian': True},
        {'name': 'Schafskäse', 'price': 7.50, 'category': 'vorspeisen', 'vegetarian': True},
        {'name': 'Pikilia kria', 'description': 'traditionelle gemischte kalte Vorspeisenplatte', 'price': 15.20, 'category': 'vorspeisen'},
        {'name': 'Dolmades', 'description': 'Weinblätter mit Reis, kalt', 'price': 6.70, 'category': 'vorspeisen', 'vegetarian': True, 'vegan': True},
        {'name': 'Dolmadakia', 'description': 'gefüllte Weinblätter mit Reis & Hackfleisch', 'price': 8.80, 'category': 'vorspeisen'},
        {'name': 'Zucchini-Bällchen', 'price': 7.80, 'category': 'vorspeisen', 'vegetarian': True},
        {'name': 'Feta aus dem Ofen', 'price': 8.90, 'category': 'vorspeisen', 'vegetarian': True},
        {'name': 'Feta Saganaki', 'price': 8.40, 'category': 'vorspeisen', 'vegetarian': True},
        {'name': 'Scampi Saganaki', 'price': 15.20, 'category': 'vorspeisen'},
        {'name': 'Octopus vom Grill', 'price': 16.20, 'category': 'vorspeisen'},
        {'name': 'Gavros Tiganitos', 'description': 'Sardellen in einer goldbraunen Hülle gebraten', 'price': 10.80, 'category': 'vorspeisen'},
        {'name': 'Pikilia Zesti', 'description': 'traditionelle gemischte warme Vorspeisenplatte', 'price': 16.20, 'category': 'vorspeisen'},
        {'name': 'Calamari Krönchen', 'price': 9.60, 'category': 'vorspeisen'},
        {'name': 'Faros', 'description': 'Käsebällchen', 'price': 11.90, 'category': 'vorspeisen', 'vegetarian': True}
    ]

    # Alle Menüpunkte zur Datenbank hinzufügen
    all_items = mittagsangebot + suppen + salate + vorspeisen

    for item_data in all_items:
        category = get_category(item_data['category'])
        if category:
            item = MenuItem(
                name=item_data['name'],
                description=item_data.get('description', ''),
                price=item_data['price'],
                category_id=category.id,
                vegetarian=item_data.get('vegetarian', False),
                vegan=item_data.get('vegan', False),
                homemade=item_data.get('homemade', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Menüpunkte (Teil 1) erfolgreich hinzugefügt!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items() 