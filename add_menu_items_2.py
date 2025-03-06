from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Fischgerichte
    fischgerichte = [
        {'name': 'Baby Calamari vom Grill', 'price': 19.20, 'category': 'fischgerichte'},
        {'name': 'Frittierte Baby Calamari', 'price': 19.20, 'category': 'fischgerichte'},
        {'name': 'Garnelen Souflaki', 'price': 22.60, 'category': 'fischgerichte'},
        {'name': 'Fischteller', 'price': 24.50, 'category': 'fischgerichte'},
        {'name': 'Dorade Royal', 'price': 24.50, 'category': 'fischgerichte'},
        {'name': 'Lachsfilet vom Grill', 'price': 22.60, 'category': 'fischgerichte'}
    ]

    # Vegetarische Gerichte
    vegetarische_gerichte = [
        {'name': 'Stamna', 'description': 'griechische Nudeln mit Gemüse und Kartoffeln', 'price': 15.90, 'category': 'vegetarische_gerichte', 'vegetarian': True},
        {'name': 'Griechische Nudeln mit Gemüse & Tomatensauce', 'price': 15.90, 'category': 'vegetarische_gerichte', 'vegetarian': True},
        {'name': 'Gemüse Ograten', 'description': 'Gemüsemischung in Schlagsahne, mit Käse überbacken', 'price': 17.50, 'category': 'vegetarische_gerichte', 'vegetarian': True}
    ]

    # Steak vom Grill
    steak_vom_grill = [
        {'name': 'Rumpsteak', 'description': 'ca. 300 g', 'price': 28.90, 'category': 'steak_vom_grill'}
    ]

    # Pfannengerichte & Ofengerichte
    pfannengerichte = [
        {'name': 'Gyros-Pfanne', 'price': 17.50, 'category': 'pfannengerichte'},
        {'name': 'Gyros überbacken mit Käse', 'price': 17.50, 'category': 'pfannengerichte'},
        {'name': 'Psaronefri-Pfanne', 'price': 19.60, 'category': 'pfannengerichte'},
        {'name': 'Musakas', 'price': 17.90, 'category': 'pfannengerichte'},
        {'name': 'Kotopulo-Pfanne', 'price': 17.80, 'category': 'pfannengerichte'},
        {'name': 'Keftedakia Smyrneika-Pfanne', 'price': 18.20, 'category': 'pfannengerichte'}
    ]

    # Alle Menüpunkte zur Datenbank hinzufügen
    all_items = fischgerichte + vegetarische_gerichte + steak_vom_grill + pfannengerichte

    for item_data in all_items:
        category = get_category(item_data['category'])
        if category:
            item = MenuItem(
                name=item_data['name'],
                description=item_data.get('description', ''),
                price=item_data['price'],
                category_id=category.id,
                vegetarian=item_data.get('vegetarian', False),
                vegan=item_data.get('vegan', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Menüpunkte (Teil 2) erfolgreich hinzugefügt!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
