from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Bier
    bier = [
        {'name': 'Helles vom Fass 0,3l', 'price': 4.20, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Helles vom Fass 0,5l', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Dunkles 0,5l', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Alkoholfreies Helles 0,3l', 'price': 3.60, 'category': 'bier', 'alcohol_free': True},
        {'name': 'Alkoholfreies Helles 0,5l', 'price': 4.50, 'category': 'bier', 'alcohol_free': True},
        {'name': 'Radler 0,5l', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Weizen vom Fass 0,3l', 'price': 3.60, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Weizen vom Fass 0,5l', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Alkoholfreies Weizen 0,5l', 'price': 4.50, 'category': 'bier', 'alcohol_free': True},
        {'name': 'Cola-Weizen 0,5l', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Russen-Halbe 0,5l', 'price': 4.50, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Pils 0,33l', 'price': 3.90, 'category': 'bier', 'contains_alcohol': True},
        {'name': 'Mytos (Griechisches Lagerbier) 0,33l', 'price': 3.90, 'category': 'bier', 'contains_alcohol': True}
    ]

    # Digestifs
    digestifs = [
        {'name': 'Tsipouro Aged', 'description': 'Gealtert in Eichenfass, Tresterbrand.', 'price': 9.00, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Mastiha Chios', 'description': 'Weltweit einzigartiger Likör aus Griechenland.', 'price': 6.70, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Rakomelo', 'description': 'Heißer Tsipouro mit Honig (Grog).', 'price': 4.00, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Averna', 'price': 4.00, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Baileys', 'price': 4.00, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Jägermeister', 'price': 3.90, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Fernet Branca', 'price': 4.00, 'category': 'digestifs', 'contains_alcohol': True},
        {'name': 'Limoncello Villa Massa', 'price': 4.00, 'category': 'digestifs', 'contains_alcohol': True}
    ]

    # Longdrinks
    longdrinks = [
        {'name': 'Ouzo-Orange', 'price': 4.00, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Gin-Tonic', 'price': 6.00, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Bacardi-Cola', 'price': 3.00, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Havana-Cola', 'price': 3.00, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Whisky-Cola', 'price': 3.00, 'category': 'longdrinks', 'contains_alcohol': True},
        {'name': 'Vodka-Lemon', 'price': 3.00, 'category': 'longdrinks', 'contains_alcohol': True}
    ]

    # Metaxa Brandy
    metaxa = [
        {'name': 'Metaxa 5 *', 'price': 12.00, 'category': 'metaxa_brandy', 'contains_alcohol': True},
        {'name': 'Metaxa 7 *', 'price': 15.00, 'category': 'metaxa_brandy', 'contains_alcohol': True},
        {'name': 'Metaxa Grand Fine Collectors Edition', 'price': 30.00, 'category': 'metaxa_brandy', 'contains_alcohol': True},
        {'name': 'Metaxa Private Reserve', 'price': 30.00, 'category': 'metaxa_brandy', 'contains_alcohol': True}
    ]

    # Beilagen
    beilagen = [
        {'name': 'Pitabrot', 'price': 3.20, 'category': 'beilagen', 'vegetarian': True},
        {'name': 'Butterreis', 'price': 3.20, 'category': 'beilagen', 'vegetarian': True},
        {'name': 'Tomatenreis', 'price': 4.00, 'category': 'beilagen', 'vegetarian': True},
        {'name': 'Pommes Frites', 'price': 4.20, 'category': 'beilagen', 'vegetarian': True},
        {'name': 'Ofenkartoffel in Folie mit Sour Cream', 'price': 4.20, 'category': 'beilagen', 'vegetarian': True},
        {'name': 'Kartoffelscheiben', 'price': 4.20, 'category': 'beilagen', 'vegetarian': True}
    ]

    # Saucen & Dips
    saucen = [
        {'name': 'Metaxa-Sauce', 'price': 6.80, 'category': 'saucen_und_dips', 'contains_alcohol': True},
        {'name': 'Senf-Sauce', 'price': 6.80, 'category': 'saucen_und_dips', 'vegetarian': True},
        {'name': 'Zitronen-Sauce', 'price': 6.80, 'category': 'saucen_und_dips', 'vegetarian': True},
        {'name': 'Rahm-Sauce', 'price': 6.80, 'category': 'saucen_und_dips', 'vegetarian': True},
        {'name': 'Ketchup', 'price': 6.80, 'category': 'saucen_und_dips', 'vegetarian': True},
        {'name': 'Mayonnaise', 'price': 6.80, 'category': 'saucen_und_dips', 'vegetarian': True}
    ]

    # Weine
    weisswein = [
        {'name': 'Thema – Assyrtiko, Sauvignon Blanc', 'description': 'Ein erfrischender griechischer Weißwein mit klaren Zitrusnoten und subtiler mineralischer Eleganz.', 'price': 25.00, 'category': 'weisswein', 'contains_alcohol': True},
        {'name': 'Amethystos – Assyrtiko, Sauvignon Blanc', 'description': 'Ein erfrischender Wein mit subtilen Noten von Zitrusfrüchten und Blüten.', 'price': 30.00, 'category': 'weisswein', 'contains_alcohol': True},
        {'name': 'Ovilos – Assyrtiko, Semillon', 'description': 'Ein eleganter Weißwein mit Nuancen von grünem Apfel und exotischen Früchten.', 'price': 60.00, 'category': 'weisswein', 'contains_alcohol': True},
        {'name': 'Magic Mountain – Sauvignon Blanc', 'description': 'Ein fruchtiger Weißwein mit Noten von Pfirsich und einer erfrischenden Säure.', 'price': 70.00, 'category': 'weisswein', 'contains_alcohol': True},
        {'name': 'Julia – Chardonnay', 'description': 'Ein harmonischer Weißwein mit fruchtigen Anklängen von Äpfeln und Birnen.', 'price': 30.00, 'category': 'weisswein', 'contains_alcohol': True},
        {'name': 'Kechribari Retsina', 'description': 'Ein einzigartiger Retsina mit frischer Pinienharznote und zitrusartiger Frische.', 'price': 15.00, 'category': 'weisswein', 'contains_alcohol': True}
    ]

    rosewein = [
        {'name': 'Amethystos – Cabernet Sauvignon, Merlot', 'description': 'Ein zarter Rosé mit Aromen von Erdbeeren und einem Hauch von Minze.', 'price': 30.00, 'category': 'rosewein', 'contains_alcohol': True},
        {'name': 'Domaine Costa Lazaridi – Merlot, Agiorgitiko, Grenache Rouge', 'description': 'Ein delikater Rosé mit frischen Erdbeer- und floralen Akzenten.', 'price': 30.00, 'category': 'rosewein', 'contains_alcohol': True},
        {'name': 'Alpha Estate – Xinomavro', 'description': 'Ein leichter Rosé mit subtilen Himbeer- und Kräuternoten.', 'price': 12.00, 'category': 'rosewein', 'contains_alcohol': True}
    ]

    rotwein = [
        {'name': 'Thema – Agiorgitiko, Syrah', 'description': 'Ein charaktervoller Rotwein, geprägt von reifen dunklen Beeren, feinen Gewürzen und sanften Tanninen.', 'price': 30.00, 'category': 'rotwein', 'contains_alcohol': True},
        {'name': 'Amethystos – Cabernet Sauvignon, Merlot, Agiorgitiko', 'description': 'Ein kräftiger Rotwein, geprägt von dunklen Beeren und einem Hauch von Vanille.', 'price': 90.00, 'category': 'rotwein', 'contains_alcohol': True},
        {'name': 'Ovilos – Cabernet Sauvignon', 'description': 'Ein intensiver Rotwein mit komplexen Aromen von schwarzen Kirschen und Gewürzen.', 'price': 90.00, 'category': 'rotwein', 'contains_alcohol': True},
        {'name': 'Magic Mountain – Cabernet Sauvignon, Cabernet Franc', 'description': 'Ein kraftvoller Rotwein mit reifen Beerenaromen und einem Hauch von Eiche.', 'price': 90.00, 'category': 'rotwein', 'contains_alcohol': True},
        {'name': 'Julia – Merlot', 'description': 'Ein ausgewogenes Rotwein mit sanften Tanninen und Noten von dunklen Beeren.', 'price': 35.00, 'category': 'rotwein', 'contains_alcohol': True},
        {'name': 'Cavino – Roditis, Savatiano', 'description': 'Süß und fruchtig, reifer Pfirsich, Aprikosen und ein Hauch von Honig.', 'price': 9.90, 'category': 'rotwein', 'contains_alcohol': True}
    ]

    # Combine all items
    all_items = bier + digestifs + longdrinks + metaxa + beilagen + saucen + weisswein + rosewein + rotwein

    for item_data in all_items:
        category = get_category(item_data['category'])
        if category:
            item = MenuItem(
                name=item_data['name'],
                description=item_data.get('description', ''),
                price=item_data['price'],
                category_id=category.id,
                vegetarian=item_data.get('vegetarian', False),
                contains_alcohol=item_data.get('contains_alcohol', False),
                alcohol_free=item_data.get('alcohol_free', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Remaining menu items added successfully!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
