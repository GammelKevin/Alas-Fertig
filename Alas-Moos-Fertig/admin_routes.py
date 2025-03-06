from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, OpeningHours, MenuItem, MenuCategory

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')

@admin_bp.route('/menu')
@login_required
def menu():
    categories = MenuCategory.query.order_by(MenuCategory.order).all()
    food_items = MenuItem.query.filter_by(is_drink=False).order_by(MenuItem.order).all()
    drink_items = MenuItem.query.filter_by(is_drink=True).order_by(MenuItem.order).all()
    return render_template('admin/menu.html', 
                         categories=categories,
                         food_items=food_items,
                         drink_items=drink_items)

@admin_bp.route('/menu/add', methods=['POST'])
@login_required
def add_menu_item():
    try:
        # Get category and determine if it's a drink
        category_id = int(request.form.get('category_id'))
        category = MenuCategory.query.get(category_id)
        if not category:
            raise ValueError('Ungültige Kategorie')

        # Get the highest order value for this category
        max_order = db.session.query(db.func.max(MenuItem.order)).filter_by(
            category_id=category_id
        ).scalar()
        
        # If no items exist yet, start with 1
        new_order = (max_order or 0) + 1

        # Create new item
        new_item = MenuItem(
            name=request.form.get('name'),
            description=request.form.get('description', ''),
            price=float(request.form.get('price')),
            category_id=category_id,
            is_drink=category.is_drink_category,
            unit=request.form.get('unit', ''),
            active=True,
            order=new_order
        )

        db.session.add(new_item)
        db.session.commit()
        flash('Menü-Item erfolgreich hinzugefügt!', 'success')
        
    except ValueError as e:
        db.session.rollback()
        flash(f'Fehler beim Hinzufügen: {str(e)}', 'error')
    except Exception as e:
        db.session.rollback()
        flash('Ein unerwarteter Fehler ist aufgetreten. Bitte überprüfen Sie alle Eingaben.', 'error')
    
    return redirect(url_for('admin.menu'))

@admin_bp.route('/menu/delete/<int:id>', methods=['POST'])
@login_required
def delete_menu_item(id):
    try:
        item = MenuItem.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        flash('Menü-Item erfolgreich gelöscht!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Fehler beim Löschen des Items.', 'error')
    return redirect(url_for('admin.menu'))

@admin_bp.route('/opening-hours')
@login_required
def opening_hours():
    hours = OpeningHours.query.order_by(OpeningHours.id).all()
    return render_template('admin/opening_hours.html', opening_hours=hours)

@admin_bp.route('/opening-hours/update', methods=['POST'])
@login_required
def update_opening_hours():
    try:
        for hour in OpeningHours.query.all():
            hour.closed = str(hour.id) in request.form.getlist('closed')
            if not hour.closed:
                hour.open_time_1 = request.form.get(f'open_time_1_{hour.id}')
                hour.close_time_1 = request.form.get(f'close_time_1_{hour.id}')
                hour.open_time_2 = request.form.get(f'open_time_2_{hour.id}')
                hour.close_time_2 = request.form.get(f'close_time_2_{hour.id}')
        db.session.commit()
        flash('Öffnungszeiten erfolgreich aktualisiert!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Speichern: {str(e)}', 'error')
    return redirect(url_for('admin.index'))
