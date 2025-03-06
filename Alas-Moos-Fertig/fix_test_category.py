from app import app, db, MenuCategory

with app.app_context():
    # Get the test category
    category = MenuCategory.query.filter_by(name='test').first()
    if category:
        # Update it to be a drink category
        category.is_drink_category = True
        db.session.commit()
        print("Successfully updated test category to be a drink category")
        
        # Verify the change
        categories = MenuCategory.query.order_by(MenuCategory.order).all()
        print("\nUpdated categories:")
        print("-------------------")
        for cat in categories:
            print(f"Name: {cat.name}, Display Name: {cat.display_name}, Order: {cat.order}, Is Drink: {cat.is_drink_category}")
    else:
        print("Category not found")
