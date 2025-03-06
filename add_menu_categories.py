from app import db, app, MenuCategory

def add_categories():
    categories = [
        {'name': 'mittagsangebot', 'display_name': 'Mittagsangebot', 'order': 1},
        {'name': 'suppen', 'display_name': 'Suppen', 'order': 2},
        {'name': 'salate', 'display_name': 'Salate', 'order': 3},
        {'name': 'vorspeisen', 'display_name': 'Vorspeisen', 'order': 4},
        {'name': 'fischgerichte', 'display_name': 'Fischgerichte', 'order': 5},
        {'name': 'vegetarische_gerichte', 'display_name': 'Vegetarische Gerichte', 'order': 6},
        {'name': 'steak_vom_grill', 'display_name': 'Steak vom Grill', 'order': 7},
        {'name': 'pfannengerichte', 'display_name': 'Pfannengerichte & Ofengerichte', 'order': 8},
        {'name': 'spezialitaeten_vom_lamm', 'display_name': 'Spezialitäten vom Lamm', 'order': 9},
        {'name': 'fleischgerichte', 'display_name': 'Fleischgerichte', 'order': 10},
        {'name': 'gemischte_fleischplatten', 'display_name': 'Gemischte Fleischplatten vom Grill', 'order': 11},
        {'name': 'desserts', 'display_name': 'Desserts', 'order': 12},
        # Getränke-Kategorien
        {'name': 'aperitifs', 'display_name': 'Aperitifs', 'order': 13},
        {'name': 'wasser_und_softdrinks', 'display_name': 'Wasser & Softdrinks', 'order': 14},
        {'name': 'saefte_und_schorlen', 'display_name': 'Säfte & Schorlen', 'order': 15},
        {'name': 'bier', 'display_name': 'Bier', 'order': 16},
        {'name': 'digestifs', 'display_name': 'Digestifs', 'order': 17},
        {'name': 'longdrinks', 'display_name': 'Longdrinks', 'order': 18},
        {'name': 'metaxa_brandy', 'display_name': 'Metaxa Brandy', 'order': 19},
        {'name': 'offene_weine', 'display_name': 'Offene Weine', 'order': 20},
        {'name': 'weinliste', 'display_name': 'Weinliste', 'order': 21},
        {'name': 'ouzo', 'display_name': 'Ouzo', 'order': 22}
    ]
    
    for cat_data in categories:
        category = MenuCategory(
            name=cat_data['name'],
            display_name=cat_data['display_name'],
            order=cat_data['order']
        )
        db.session.add(category)
    
    db.session.commit()
    print("Kategorien erfolgreich hinzugefügt!")

if __name__ == '__main__':
    with app.app_context():
        # Bestehende Kategorien löschen
        MenuCategory.query.delete()
        db.session.commit()
        
        # Neue Kategorien hinzufügen
        add_categories() 