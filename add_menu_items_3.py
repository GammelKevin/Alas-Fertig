from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Spezialitäten vom Lamm
    spezialitaeten_vom_lamm = [
        {'name': 'Lammkoteletts', 'price': 19.90, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Zarte Lammhaxen aus dem Backofen (mit grünen Bohnen)', 'price': 21.60, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Zarte Lammhaxen aus dem Backofen (mit dicken Bohnen)', 'price': 21.20, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Zarte Lammhaxen aus dem Backofen (mit Bamies)', 'price': 21.60, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Zarte Lammhaxen aus dem Backofen (mit Spaghetti)', 'price': 21.20, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Stifado', 'description': 'zartes Lammfleisch mit Schalotten in Tomaten-Kräutersauce', 'price': 19.90, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Kleftiko', 'price': 21.60, 'category': 'spezialitaeten_vom_lamm'}
    ]

    # Fleischgerichte
    fleischgerichte = [
        {'name': 'Sutzukakia', 'description': 'gegrillte Hackfleischröllchen', 'price': 14.90, 'category': 'fleischgerichte'},
        {'name': 'Gyros', 'price': 15.90, 'category': 'fleischgerichte', 'homemade': True},
        {'name': 'Souflaki', 'description': 'zwei Spieße', 'price': 15.90, 'category': 'fleischgerichte'},
        {'name': 'Bifteki', 'description': 'Hacksteak gefüllt mit Schafskäse', 'price': 17.50, 'category': 'fleischgerichte'},
        {'name': 'Hähnchenfilet', 'price': 15.60, 'category': 'fleischgerichte'},
        {'name': 'Bauernspieß', 'price': 20.50, 'category': 'fleischgerichte'},
        {'name': 'Kalbsleber', 'price': 17.50, 'category': 'fleischgerichte'},
        {'name': 'Rückensteak vom Grill', 'price': 17.50, 'category': 'fleischgerichte'},
        {'name': 'Medaillons vom Grill', 'price': 19.60, 'category': 'fleischgerichte'},
        {'name': 'Schnitzel Wiener Art', 'price': 16.80, 'category': 'fleischgerichte'}
    ]

    # Gemischte Fleischplatten vom Grill
    gemischte_fleischplatten = [
        {'name': 'Mia-Platte', 'price': 17.20, 'category': 'gemischte_fleischplatten'},
        {'name': 'Alas-Platte', 'price': 19.90, 'category': 'gemischte_fleischplatten'},
        {'name': 'Meteora-Platte', 'price': 17.80, 'category': 'gemischte_fleischplatten'},
        {'name': 'Trikala-Platte', 'price': 17.90, 'category': 'gemischte_fleischplatten'},
        {'name': 'Thessalia-Platte', 'price': 17.90, 'category': 'gemischte_fleischplatten'},
        {'name': 'Volos-Platte', 'price': 17.20, 'category': 'gemischte_fleischplatten'},
        {'name': 'Dorf-Platte', 'price': 19.90, 'category': 'gemischte_fleischplatten'}
    ]

    # Desserts
    desserts = [
        {'name': 'Griechischer Joghurt mit Honig & Walnüssen', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Galaktoboureko', 'description': 'Blätterteig mit Vanilleeis-Grießcreme gefüllt & Vanilleeis', 'price': 8.30, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Mille-Feuille', 'description': 'Blätterteig gefüllt mit Vanillecreme, Erdbeeren & Pistazien', 'price': 8.30, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Steirer-Eis', 'description': 'Vanilleeis mit Kürbiskernöl & karamellisierten Kürbiskernen', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Coupé Ananas', 'description': 'Vanilleeis mit frischer Ananas & Schlagsahne', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Heiße Feigen', 'description': 'gekocht in Cassis-Likör & Vanilleeis', 'price': 8.30, 'category': 'desserts', 'vegetarian': True, 'contains_alcohol': True},
        {'name': 'Eis mit heißen Himbeeren', 'description': 'Vanilleeis mit heißen Himbeeren & Sahne', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Gemischtes Eis', 'description': 'Vanille-, Erdbeer- und Schokoladeneis, dazu Sahne', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Gadaifi', 'description': 'Knusprige Teigfäden mit Walnussfüllung und Zuckersirup, dazu Vanilleeis', 'price': 8.30, 'category': 'desserts', 'vegetarian': True}
    ]

    # Alle Menüpunkte zur Datenbank hinzufügen
    all_items = spezialitaeten_vom_lamm + fleischgerichte + gemischte_fleischplatten + desserts

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
                homemade=item_data.get('homemade', False),
                contains_alcohol=item_data.get('contains_alcohol', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Menüpunkte (Teil 3) erfolgreich hinzugefügt!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
