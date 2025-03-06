from app import db, app, MenuCategory, MenuItem

def add_categories():
    categories = [
        {'name': 'mittagsangebot', 'display_name': 'Mittagsangebot', 'order': 1},
        {'name': 'aperitifs', 'display_name': 'Aperitifs', 'order': 2},
        {'name': 'suppen', 'display_name': 'Suppen', 'order': 3},
        {'name': 'salate', 'display_name': 'Salate', 'order': 4},
        {'name': 'fischgerichte', 'display_name': 'Fischgerichte', 'order': 5},
        {'name': 'vegetarische_gerichte', 'display_name': 'Vegetarische Gerichte', 'order': 6},
        {'name': 'steak_vom_grill', 'display_name': 'Steak vom Grill', 'order': 7},
        {'name': 'pfannengerichte', 'display_name': 'Pfannengerichte', 'order': 8},
        {'name': 'spezialitaeten_vom_lamm', 'display_name': 'Spezialitäten vom Lamm', 'order': 9},
        {'name': 'fleischgerichte', 'display_name': 'Fleischgerichte', 'order': 10},
        {'name': 'gemischte_fleischplatten', 'display_name': 'Gemischte Fleischplatten', 'order': 11},
        {'name': 'desserts', 'display_name': 'Desserts', 'order': 12},
        {'name': 'kaffee_und_tee', 'display_name': 'Kaffee & Tee', 'order': 13},
        {'name': 'wasser_und_softdrinks', 'display_name': 'Wasser & Softdrinks', 'order': 14, 'is_drink_category': True},
        {'name': 'bier', 'display_name': 'Bier', 'order': 15, 'is_drink_category': True},
        {'name': 'digestifs', 'display_name': 'Digestifs', 'order': 16, 'is_drink_category': True},
        {'name': 'longdrinks', 'display_name': 'Longdrinks', 'order': 17, 'is_drink_category': True},
        {'name': 'metaxa_brandy', 'display_name': 'Metaxa Brandy', 'order': 18, 'is_drink_category': True},
        {'name': 'beilagen', 'display_name': 'Beilagen', 'order': 19},
        {'name': 'saucen_und_dips', 'display_name': 'Saucen & Dips', 'order': 20},
        {'name': 'weisswein', 'display_name': 'Weißwein', 'order': 21, 'is_drink_category': True},
        {'name': 'rosewein', 'display_name': 'Roséwein', 'order': 22, 'is_drink_category': True},
        {'name': 'rotwein', 'display_name': 'Rotwein', 'order': 23, 'is_drink_category': True}
    ]
    
    for cat_data in categories:
        category = MenuCategory(
            name=cat_data['name'],
            display_name=cat_data['display_name'],
            order=cat_data['order'],
            is_drink_category=cat_data.get('is_drink_category', False)
        )
        db.session.add(category)
    
    db.session.commit()
    print("Categories added successfully!")

if __name__ == '__main__':
    with app.app_context():
        # Clear existing categories
        MenuCategory.query.delete()
        db.session.commit()
        
        # Add new categories
        add_categories()
