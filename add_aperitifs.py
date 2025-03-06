from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Aperitifs category
    aperitifs_category = MenuCategory(
        name="Aperitifs",
        display_name="Aperitifs",
        description="Traditionelle griechische und internationale Aperitifs",
        order=2,
        is_drink_category=True
    )
    
    # Add the category to the database
    db.session.add(aperitifs_category)
    db.session.commit()
    
    print(f"Category 'Aperitifs' created with ID: {aperitifs_category.id}")
    
    # Now add all the Aperitifs items
    aperitifs_items = [
        MenuItem(
            name="01. Tsipouro mit oder ohne Anis",
            description="Traditioneller griechischer Tresterbrand",
            price=3.9,
            category_id=aperitifs_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="02. Ouzo",
            description="Klassischer griechischer Anisschnaps",
            price=3.9,
            category_id=aperitifs_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="12. Ouzo rose mit Rosen Likör",
            description="Ouzo verfeinert mit Rosenlikör",
            price=4.0,
            category_id=aperitifs_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="03. Ouzo mit Olive oder Feige",
            description="Ouzo serviert mit Olive oder Feige",
            price=4.2,
            category_id=aperitifs_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="04. Ouzo mit Eiswürfeln",
            description="Klassischer Ouzo, serviert mit Eiswürfeln",
            price=3.9,
            category_id=aperitifs_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="05. Martini Bianco oder Rosso",
            description="Italienischer Wermut, wahlweise weiß oder rot",
            price=4.5,
            category_id=aperitifs_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="06. Orange- oder Sekt",
            description="Erfrischender Sekt mit Orange",
            price=4.5,
            category_id=aperitifs_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="07. Lillet Wild Berry",
            description="Französischer Aperitif mit Wildbeeren",
            price=4.5,
            category_id=aperitifs_category.id,
            contains_alcohol=True
        ),
        MenuItem(
            name="08. Campari",
            description="Italienischer Bitterlikör",
            price=3.9,
            category_id=aperitifs_category.id,
            contains_alcohol=True
        )
    ]
    
    # Add all items at once
    db.session.add_all(aperitifs_items)
    db.session.commit()
    
    print(f"Added {len(aperitifs_items)} menu items to 'Aperitifs' category")
    
print("Done!") 