from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Aperitifs
    aperitifs = [
        {'name': 'Tsipouro mit oder ohne Anis', 'price': 3.50, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Ouzo', 'price': 3.50, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Ouzo rose mit Rosen Likör', 'price': 3.90, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Ouzo mit Olive oder Feige', 'price': 3.50, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Ouzo mit Eiswürfeln', 'price': 3.50, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Martini Bianco oder Rosso Campari', 'price': 3.50, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Orange oder Sekt', 'price': 3.50, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Lillet wild berry', 'price': 3.50, 'category': 'aperitifs', 'contains_alcohol': True}
    ]

    # Wasser & Softdrinks
    wasser_und_softdrinks = [
        {'name': 'Adldorfer Gourmet Natur (0,25 l)', 'price': 3.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Adldorfer Gourmet Natur (0,75 l)', 'price': 6.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Adldorfer Gourmet Klassik (0,25 l)', 'price': 3.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Adldorfer Gourmet Klassik (0,75 l)', 'price': 6.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Griechisches Wasser Still (0,5 l)', 'price': 4.80, 'category': 'wasser_und_softdrinks'},
        {'name': 'Tafelwasser (0,4 l)', 'price': 4.50, 'category': 'wasser_und_softdrinks'},
        {'name': 'Cola, Orangenlimo, Zitronenlimo, Spezi (0,2 l)', 'price': 3.90, 'category': 'wasser_und_softdrinks'},
        {'name': 'Cola, Orangenlimo, Zitronenlimo, Spezi (0,4 l)', 'price': 4.50, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola Zero (0,2 l)', 'price': 3.90, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola Zero (0,4 l)', 'price': 4.50, 'category': 'wasser_und_softdrinks'}
    ]

    # Säfte & Schorlen
    saefte_und_schorlen = [
        {'name': 'Apfel/Johannisbeere/Maracuja/Traube (aus Nektar und Saftkonzentrat)', 'price': 6.00, 'category': 'saefte_und_schorlen'},
        {'name': 'Orangensaft', 'price': 6.00, 'category': 'saefte_und_schorlen'},
        {'name': 'Saftschorle (Apfel/Johannisbeere/Maracuja/Traube)', 'price': 6.00, 'category': 'saefte_und_schorlen'},
        {'name': 'Holunderschorle', 'price': 9.00, 'category': 'saefte_und_schorlen'}
    ]

    # Bier
    bier = [
        {'name': 'Helles vom Fass (0,2 l)', 'price': 3.60, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Helles vom Fass (0,4 l)', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Alkoholfreies Helles (0,3 l)', 'price': 3.60, 'category': 'bier', 'alcohol_free': True},
        {'name': 'Dunkles (0,5 l)', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Radler (0,5 l)', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Weizen vom Fass (0,3 l)', 'price': 3.60, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Weizen vom Fass (0,5 l)', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Alkoholfreies Weizen (0,5 l)', 'price': 4.50, 'category': 'bier', 'alcohol_free': True},
        {'name': 'Cola-Weizen (0,5 l)', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Russen-Halbe (0,5 l)', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Pils (0,33 l)', 'price': 3.90, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Mytos (0,33 l)', 'price': 3.90, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Griechisches Lagerbier (0,5 l)', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True}
    ]

    # Alle Menüpunkte zur Datenbank hinzufügen
    all_items = aperitifs + wasser_und_softdrinks + saefte_und_schorlen + bier

    for item_data in all_items:
        category = get_category(item_data['category'])
        if category:
            item = MenuItem(
                name=item_data['name'],
                description=item_data.get('description', ''),
                price=item_data['price'],
                category_id=category.id,
                alcohol_free=item_data.get('alcohol_free', False),
                contains_alcohol=item_data.get('contains_alcohol', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Menüpunkte (Teil 4) erfolgreich hinzugefügt!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
