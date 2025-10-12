import os
from datetime import datetime

from flask import Blueprint, render_template, send_file
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from reportlab.lib.pagesizes import A4

from models.product import Shoe
from models.user import User
from models.order import Order, OrderItem
from models import db
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from services.product_service import add_new_product

cart_bp = Blueprint('cart', __name__)
PRODUCT_IMAGES = {
    'nike_air_force_1': 'air_force_1.jpg',
    'adidas_ultraboost': 'adidas_ultraboost_1.jpg',
    'puma_rs-x': 'puma_rs_x.jpg',
    'adidas_predator': 'adidas_predator.jpg',
    'nike_air_max': 'air_max.jpg',
    'clarks_oxford': 'clarks_oxford.jpg',
    'hugo_boss_boss_classic': 'hugo_boss_boss_classic.jpg',
    'geox_derby': 'geox_derby.jpg',
    'salvatore_monk_strap': 'salvatore_monk_strap.jpg',
    'adidas_superstar': 'adidas_superstar.jpg',
    'new_balance_574': 'new_balance_574.jpg',
    'vans_old_skool': 'vans_old_skool.jpg',
    'converse_chuck_70': 'converse_chuck_70.jpg',
    'clarks_desert_boot': 'clarks_desert_boot.jpg'
}

@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = session.get('cart', [])
    if cart_items:
        total = 0
        order = Order(user_id=current_user.id, total=0, status='обработва се')
        db.session.add(order)
        db.session.flush()

        for product_id in cart_items:
            try:
                product_db_id = int(product_id.split('_')[-1])
                product = Shoe.query.get(product_db_id)
                if product and product.in_stock > 0:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=1,
                        price=product.price
                    )
                    total += product.price
                    product.in_stock -= 1
                    db.session.add(order_item)
            except (ValueError, IndexError):
                continue

        order.total = total
        db.session.commit()
        flash(f'Поръчка #{order.id} е успешно направена!', 'success')
    else:
        flash('Количката ви е празна!', 'warning')

    session['cart'] = []
    return redirect(url_for('cart.cart_page'))

@cart_bp.route('dashboard/cart')
@login_required
def cart_page():
    cart_items = session.get('cart', [])

    valid_cart_items = []
    for product_id in cart_items:
        try:
            product_db_id = int(product_id.split('_')[-1])
            product = Shoe.query.get(product_db_id)
            if product and product.in_stock > 0:
                valid_cart_items.append(product_id)
        except (ValueError, IndexError):
            continue

    if len(valid_cart_items) != len(cart_items):
        session['cart'] = valid_cart_items
        session.modified = True

    products_dict = {}
    for product_id in valid_cart_items:
        try:
            product_db_id = int(product_id.split('_')[-1])
            product = Shoe.query.get(product_db_id)
            if product:
                products_dict[product_id] = product
        except (ValueError, IndexError):
            continue

    return render_template(
        "dashboard/cart.html",
        current_user=current_user,
        cart_items=valid_cart_items,
        products_dict=products_dict,
        product_images = PRODUCT_IMAGES
    )

@cart_bp.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')

    if not product_id:
        flash('Невалиден продукт!', 'error')
        return redirect(url_for('dashboard.dashboard'))

    try:
        product_db_id = int(product_id.split('_')[-1])
        product = Shoe.query.get(product_db_id)
        if not product:
            flash('Продуктът не е намерен!', 'error')
            return redirect(url_for('dashboard.dashboard'))

        if product.in_stock <= 0:
            flash('Продуктът е изчерпан!', 'warning')
            return redirect(url_for('dashboard.dashboard'))
    except (ValueError, IndexError):
        flash('Невалиден продукт!', 'error')
        return redirect(url_for('dashboard.dashboard'))

    if 'cart' not in session:
        session['cart'] = []

    if product_id not in session['cart']:
        session['cart'].append(product_id)
        session.modified = True
        flash(f'{product.name} е добавен в количката!', 'success')
    else:
        flash('Продуктът вече е в количката!', 'info')

    return redirect(url_for('dashboard.dashboard'))

@cart_bp.route('/clear_cart')
@login_required
def clear_cart():
    if 'cart' in session:
        session['cart'] = []
        session.modified = True
        flash('Количката е изчистена!', 'success')
    return redirect(url_for('cart.cart_page'))

@cart_bp.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    product_id = request.form.get('product_id')

    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        session.modified = True
        flash('Продуктът е премахнат от количката!', 'success')

    return redirect(url_for('cart.cart_page'))


@cart_bp.route('/convert_to_pdf', methods=['POST'])
@login_required
def convert_to_pdf():
    try:
        user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()

        if not user_orders:
            flash('Нямате поръчки за експорт.', 'warning')
            return redirect(url_for('cart.cart_page'))

        filename = f"order_report_{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join('static', 'pdf', filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "ORDER DETAILS")
        c.drawString(50, height - 80, f"USER: {current_user.username}")
        c.drawString(50, height - 100, f"Date of generating: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        c.line(50, height - 120, width - 50, height - 120)

        y_position = height - 150

        for i, order in enumerate(user_orders):
            if y_position < 100:
                c.showPage()
                y_position = height - 50

            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, f"Order #{order.id}")
            y_position -= 25

            c.setFont("Helvetica", 10)
            c.drawString(50, y_position, f"Date of order: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
            y_position -= 15
            c.drawString(50, y_position, f"Status: {order.status}")
            y_position -= 15
            c.drawString(50, y_position, f"Total price: {order.total:.2f} лв")
            y_position -= 25

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_position, "Products:")
            y_position -= 20

            for item in order.items:
                if y_position < 100:
                    c.showPage()
                    y_position = height - 50
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(50, y_position, "Products(continuing:")
                    y_position -= 20

                c.setFont("Helvetica-Bold", 10)
                c.drawString(70, y_position, f"▪ {item.product.name}")
                y_position -= 15

                c.setFont("Helvetica", 9)
                c.drawString(90, y_position, f"Brand: {item.product.brand}")
                y_position -= 12
                c.drawString(90, y_position, f"Category: {item.product.category}")
                y_position -= 12
                c.drawString(90, y_position, f"Colour: {item.product.color}, Size: {item.product.size}")
                y_position -= 12
                c.drawString(90, y_position, f"Price: {item.price:.2f} lv x {item.quantity}")
                y_position -= 12
                c.drawString(90, y_position, f"Total: {item.price * item.quantity:.2f} lv")
                y_position -= 20
            if i < len(user_orders) - 1:
                c.line(50, y_position, width - 50, y_position)
                y_position -= 30
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Summary")

        total_orders = len(user_orders)
        total_amount = sum(order.total for order in user_orders)
        total_items = sum(len(order.items) for order in user_orders)

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, f"Total orders count: {total_orders}")
        c.drawString(50, height - 120, f"Total products count: {total_items}")
        c.drawString(50, height - 140, f"Total price: {total_amount:.2f} lv")
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(50, 30, f"Generetaed by the T-Shoe system on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        c.save()
        return send_file(filepath, as_attachment=True, download_name=filename)

    except Exception as e:
        flash(f'Грешка при генериране на PDF: {str(e)}', 'error')
        return redirect(url_for('cart.cart_page'))


