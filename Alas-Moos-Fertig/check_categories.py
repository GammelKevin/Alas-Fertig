from app import app, db, MenuCategory

with app.app_context():
    categories = MenuCategory.query.order_by(MenuCategory.order).all()
    print("\nCategories in order:")
    print("-------------------")
    for cat in categories:
        print(f"Name: {cat.name}, Display Name: {cat.display_name}, Order: {cat.order}, Is Drink: {cat.is_drink_category}")
