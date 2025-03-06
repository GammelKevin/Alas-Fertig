from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Desserts
    desserts = [
        {'name': 'Griechischer Joghurt', 'description': 'Mit Honig & Walnüssen.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Galaktoboureko', 'description': 'Blätterteig mit Vanilleeis-Grießcreme gefüllt & Vanilleeis.', 'price': 8.30, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Mille-feuille', 'description': 'Blätterteig gefüllt mit Vanillecreme, Erdbeeren & Pistazien.', 'price': 8.30, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Steirer-Eis', 'description': 'Vanilleeis mit Kürbiskernöl & karamellisierten Kürbiskernen.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Coupé Ananas', 'description': 'Vanilleeis mit frischer Ananas & Schlagsahne.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Heiße Feigen', 'description': 'Heiße Feigen gekocht in Cassis-Likör & Vanilleeis.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True, 'contains_alcohol': True},
        {'name': 'Eis mit heißen Himbeeren', 'description': 'Vanilleeis mit heißen Himbeeren & Sahne.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Gemischtes Eis', 'description': 'Vanille-, Erdbeer- und Schokoladeneis, dazu Sahne.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Gadaifi', 'description': 'Knusprige Teigfäden mit Walnussfüllung und Zuckersirup, dazu Vanilleeis.', 'price': 8.30, 'category': 'desserts', 'vegetarian': True}
    ]

    # Kaffee & Tee
    kaffee_tee = [
        {'name': 'Espresso', 'price': 3.50, 'category': 'kaffee_und_tee'},
        {'name': 'Espresso Doppio', 'price': 3.50, 'category': 'kaffee_und_tee'},
        {'name': 'Espresso Macchiato', 'price': 3.50, 'category': 'kaffee_und_tee'},
        {'name': 'Affogato Espresso', 'price': 3.50, 'category': 'kaffee_und_tee'},
        {'name': 'Cappuccino', 'price': 3.60, 'category': 'kaffee_und_tee'},
        {'name': 'Latte Macchiato', 'price': 3.60, 'category': 'kaffee_und_tee'},
        {'name': 'Griechischer Mokka', 'price': 3.00, 'category': 'kaffee_und_tee'},
        {'name': 'Tasse Kaffee', 'price': 0.50, 'category': 'kaffee_und_tee'},
        {'name': 'Tasse Tee', 'price': 0.50, 'category': 'kaffee_und_tee'},
        {'name': 'Frappe', 'price': 3.00, 'category': 'kaffee_und_tee'},
        {'name': 'Eis-Schokolade', 'description': 'Mit Vanilleeis, Schokoladensauce & Sahne.', 'price': 6.70, 'category': 'kaffee_und_tee'},
        {'name': 'Eis-Kaffee', 'description': 'Mit Vanilleeis & Sahne.', 'price': 6.70, 'category': 'kaffee_und_tee'}
    ]

    # Wasser & Softdrinks
    getraenke = [
        {'name': 'Adldorfer Gourmet Natur 0,25l', 'price': 3.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Adldorfer Gourmet Natur 0,75l', 'price': 6.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Adldorfer Gourmet Klassik 0,25l', 'price': 3.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Adldorfer Gourmet Klassik 0,75l', 'price': 6.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Griechisches Wasser Still 0,5l', 'price': 4.80, 'category': 'wasser_und_softdrinks'},
        {'name': 'Tafelwasser 0,4l', 'price': 4.50, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola 0,2l', 'price': 3.90, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola 0,4l', 'price': 4.50, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola Zero 0,2l', 'price': 3.90, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola Zero 0,4l', 'price': 4.50, 'category': 'wasser_und_softdrinks'},
        {'name': 'Apfelschorle', 'price': 6.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Holunderschorle', 'price': 9.00, 'category': 'wasser_und_softdrinks'}
    ]

    # Digestifs
    digestifs = [
        {'name': 'Tsipouro Aged', 'description': 'Gealtert in Eichenfass, Tresterbrand', 'price': 9.00, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Mastiha Chios', 'description': 'weltweit einzigartiger Likör aus Griechenland', 'price': 9.00, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Rakomelo', 'description': 'heißer Tsipouro mit Honig (Grog) - 4cl', 'price': 9.00, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Averna - 4cl', 'price': 6.70, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Baileys - 4cl', 'price': 6.70, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Jägermeister - 2cl', 'price': 3.90, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Fernet Branca - 2cl', 'price': 3.90, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Ramazzotti - 4cl', 'price': 3.90, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Limoncello Villa Massa - 4cl', 'price': 6.70, 'category': 'digestifs', 'contains_alcohol': True}
    ]

    # Longdrinks
    longdrinks = [
        {'name': 'Ouzo-Orange', 'price': 3.90, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Gin-Tonic', 'price': 6.70, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Bacardi-Cola', 'price': 3.00, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Havana-Cola', 'price': 3.00, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Whisky-Cola', 'price': 3.00, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Vodka-Lemon', 'price': 3.00, 'category': 'longdrinks', 'contains_alcohol': True}
    ]

    # Metaxa Brandy
    metaxa_brandy = [
        {'name': 'Metaxa 5*', 'price': 30.00, 'category': 'metaxa_brandy', 'contains_alcohol': True},
        {'name': 'Metaxa 7*', 'price': 60.00, 'category': 'metaxa_brandy', 'contains_alcohol': True},
        {'name': 'Metaxa Grand Fine Collectors Edition', 'price': 90.00, 'category': 'metaxa_brandy', 'contains_alcohol': True},
        {'name': 'Metaxa Private Reserve', 'price': 90.00, 'category': 'metaxa_brandy', 'contains_alcohol': True}
    ]

    # Offene Weine
    offene_weine = [
        {'name': 'Rotwein Imiglikos (halbsüß - Tafelwein) - 0,2 l', 'price': 5.50, 'category': 'offene_weine', 'contains_alcohol': True},
        {'name': 'Rotwein Hauswein (Trocken-Qualitätswein) - 0,2 l', 'price': 5.50, 'category': 'offene_weine', 'contains_alcohol': True},
        {'name': 'Mavrodafni (Dessertwein) - 0,2 l', 'price': 6.00, 'category': 'offene_weine', 'contains_alcohol': True},
        {'name': 'Roséwein Imiglikos (halbsüß - Tafelwein) - 0,2 l', 'price': 5.50, 'category': 'offene_weine', 'contains_alcohol': True},
        {'name': 'Roséwein Hauswein (Trocken-Qualitätswein) - 0,2 l', 'price': 5.50, 'category': 'offene_weine', 'contains_alcohol': True},
        {'name': 'Weißwein Imiglikos (halbsüß - Tafelwein) - 0,2 l', 'price': 5.50, 'category': 'offene_weine', 'contains_alcohol': True},
        {'name': 'Weißwein Hauswein (Trocken-Qualitätswein) - 0,2 l', 'price': 5.50, 'category': 'offene_weine', 'contains_alcohol': True},
        {'name': 'Retsina - Malamatina (geharzt) - 0,2 l', 'price': 5.50, 'category': 'offene_weine', 'contains_alcohol': True},
        {'name': 'Muscat aus Patras (Dessertwein) - 0,2 l', 'price': 6.00, 'category': 'offene_weine', 'contains_alcohol': True},
        {'name': 'Weinschorle - 0,2 l', 'price': 5.50, 'category': 'offene_weine', 'contains_alcohol': True}
    ]

    # Weinliste
    weinliste = [
        {'name': 'THEMA - ASSYRTIKO, SAUVIGNON BLANC', 'price': 25.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'AMETHISTOS - ASSYRTIKO, SAUVIGNON BLANC', 'price': 30.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'OVILOS - ASSYRTIKO, SEMILLON', 'price': 30.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'MAGIC MOUNTAIN - SAUVIGNON BLANC', 'price': 30.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'JULIA - CHARDONNAY', 'price': 15.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'KECHRIBARI RETSINA', 'price': 15.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'AMETHISTOS - CABERNET SAUVIGNON, MERLOT', 'price': 30.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'DOMAINE COSTA LAZARIDI - MERLOT, AGIORITIKO, GRENACHE ROUGE', 'price': 30.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'ALPHA ESTATE - XINOMAVRO', 'price': 12.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'THEMA - AGIORITIKO, SYRAH', 'price': 30.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'AMETHISTOS - CABERNET SAUVIGNON, MERLOT, AGIORITIKO', 'price': 40.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'OVILOS - CABERNET SAUVIGNON', 'price': 40.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'MAGIC MOUNTAIN - CABERNET SAUVIGNON, CABERNET FRANC', 'price': 90.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'JULIA - MERLOT', 'price': 30.00, 'category': 'weinliste', 'contains_alcohol': True},
        {'name': 'CAVINO - RODITIS, SAVATIANO', 'price': 9.90, 'category': 'weinliste', 'contains_alcohol': True}
    ]

    # Ouzo
    ouzo = [
        {'name': 'PLOMARI OUZO (0,2L)', 'price': 30.00, 'category': 'ouzo', 'contains_alcohol': True},
        {'name': 'PLOMARI OUZO (0,7L)', 'price': 60.00, 'category': 'ouzo', 'contains_alcohol': True},
        {'name': 'KATSAROS OUZO (50ML)', 'price': 6.50, 'category': 'ouzo', 'contains_alcohol': True},
        {'name': 'KATSAROS OUZO (0,7L)', 'price': 90.00, 'category': 'ouzo', 'contains_alcohol': True}
    ]

    # Combine all items
    all_items = desserts + kaffee_tee + getraenke + digestifs + longdrinks + metaxa_brandy + offene_weine + weinliste + ouzo

    for item_data in all_items:
        category = get_category(item_data['category'])
        if category:
            item = MenuItem(
                name=item_data['name'],
                description=item_data.get('description', ''),
                price=item_data['price'],
                category_id=category.id,
                vegetarian=item_data.get('vegetarian', False),
                contains_alcohol=item_data.get('contains_alcohol', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Desserts and beverages added successfully!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
