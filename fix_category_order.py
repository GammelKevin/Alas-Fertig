from app import app, db, MenuCategory

with app.app_context():
    # Get the category
    category = MenuCategory.query.filter_by(name='cocktail').first()
    if category:
        # Update the order to 5 (after Getränke)
        category.order = 5
        db.session.commit()
        print("Successfully updated category order")
        
        # Verify the change
        categories = MenuCategory.query.order_by(MenuCategory.order).all()
        print("\nUpdated categories in order:")
        print("-------------------")
        for cat in categories:
            print(f"Name: {cat.name}, Display Name: {cat.display_name}, Order: {cat.order}, Is Drink: {cat.is_drink_category}")
    else:
        print("Category not found")
