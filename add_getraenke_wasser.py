from app import app, db
from models import MenuCategory, MenuItem

# Create application context
with app.app_context():
    # Create the Wasser & Softdrinks category
    wasser_category = MenuCategory(
        name="Wasser & Softdrinks",
        display_name="Wasser & Softdrinks",
        description="Erfrischende alkoholfreie Getränke",
        order=14,
        is_drink_category=True
    )
    
    db.session.add(wasser_category)
    db.session.commit()
    
    print(f"Category 'Wasser & Softdrinks' created with ID: {wasser_category.id}")
    
    # Add Wasser & Softdrinks items
    wasser_items = [
        MenuItem(
            name="280. Adldorfer Gourmet Natur 0,25l",
            description="Stilles Mineralwasser",
            price=3.0,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="280. Adldorfer Gourmet Natur 0,75l",
            description="Stilles Mineralwasser",
            price=6.0,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="281. Adldorfer Gourmet Klassik 0,25l",
            description="Mineralwasser mit Kohlensäure",
            price=3.0,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="281. Adldorfer Gourmet Klassik 0,75l",
            description="Mineralwasser mit Kohlensäure",
            price=6.0,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="282. Griechisches Wasser Still 0,5l",
            description="Stilles Wasser aus Griechenland",
            price=4.8,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="283. Tafelwasser 0,4l",
            description="Aufbereitetes Trinkwasser",
            price=4.5,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="284. Coca Cola 0,2l",
            description="Klassische Cola",
            price=3.9,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="284. Coca Cola 0,4l",
            description="Klassische Cola",
            price=4.5,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="284. Orangenlimo 0,2l",
            description="Erfrischende Orangenlimonade",
            price=3.9,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="284. Orangenlimo 0,4l",
            description="Erfrischende Orangenlimonade",
            price=4.5,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="284. Zitronenlimo 0,2l",
            description="Erfrischende Zitronenlimonade",
            price=3.9,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="284. Zitronenlimo 0,4l",
            description="Erfrischende Zitronenlimonade",
            price=4.5,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="284. Spezi 0,2l",
            description="Cola-Orangenlimo-Mix",
            price=3.9,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="284. Spezi 0,4l",
            description="Cola-Orangenlimo-Mix",
            price=4.5,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="285. Coca Cola Zero 0,2l",
            description="Zuckerfreie Cola",
            price=3.9,
            category_id=wasser_category.id,
            alcohol_free=True,
            sugar_free=True
        ),
        MenuItem(
            name="285. Coca Cola Zero 0,4l",
            description="Zuckerfreie Cola",
            price=4.5,
            category_id=wasser_category.id,
            alcohol_free=True,
            sugar_free=True
        ),
        MenuItem(
            name="286. Apfelschorle",
            description="Apfelsaft mit Mineralwasser",
            price=6.0,
            category_id=wasser_category.id,
            alcohol_free=True
        ),
        MenuItem(
            name="287. Holunderschorle",
            description="Holundersaft mit Mineralwasser",
            price=9.0,
            category_id=wasser_category.id,
            alcohol_free=True
        )
    ]
    
    db.session.add_all(wasser_items)
    db.session.commit()
    
    print(f"Added {len(wasser_items)} menu items to 'Wasser & Softdrinks' category")
    
print("Done!") 