from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models.user import current_user, accounts
from models.order import products_dict, all_products, orders, CATEGORIES, BRANDS
from services.product_service import get_filtered_products, add_new_product
from services.notification_service import (
    add_product_notification, get_unread_notifications,
    mark_notification_as_read, mark_all_notifications_as_read
)

dashboard_bp = Blueprint('dashboard', __name__)

PRODUCT_IMAGES = {
    'nike_air_force_1_0': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop',
    'adidas_ultraboost_1': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=300&fit=crop',
    'puma_rs-x_2': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&h=300&fit=crop',
    'adidas_predator_3': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop',
    'nike_air_max_4': 'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400&h=300&fit=crop',
    'clarks_oxford_5': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=300&fit=crop',
    'hugo_boss_boss_classic_6': 'https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=400&h=300&fit=crop',
    'geox_derby_7': 'https://images.unsplash.com/photo-1531315630201-bb15abeb1653?w=400&h=300&fit=crop',
    'salvatore_monk_strap_8': 'https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=400&h=300&fit=crop',
    'adidas_superstar_9': 'https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?w=400&h=300&fit=crop',
    'new_balance_574_10': 'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400&h=300&fit=crop',
    'vans_old_skool_11': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop',
    'converse_chuck_70_12': 'https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=400&h=300&fit=crop',
    'clarks_desert_boot_13': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=300&fit=crop'
}


@dashboard_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Моля, влезте в системата, за да видите дашборда.', 'warning')
        return redirect(url_for('auth.login'))

    search_term = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    subcategory_filter = request.args.get('subcategory', '')
    brand_filter = request.args.get('brand', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')

    filtered_products = get_filtered_products(
        search_term, category_filter, subcategory_filter,
        brand_filter, min_price, max_price
    )

    current_user.username = session['username']
    unread_notifications = get_unread_notifications(session.get('username'))

    return render_template('dashboard/dashboard.html',
                           current_user=current_user,
                           products_dict=filtered_products,
                           product_images=PRODUCT_IMAGES,
                           categories=CATEGORIES,
                           brands=BRANDS,
                           search_term=search_term,
                           category_filter=category_filter,
                           subcategory_filter=subcategory_filter,
                           brand_filter=brand_filter,
                           min_price=min_price,
                           max_price=max_price,
                           unread_notifications=unread_notifications)


@dashboard_bp.route('/dashboard/cart')
def cart_page():
    if 'username' not in session:
        flash('Моля, влезте в системата.', 'warning')
        return redirect(url_for('auth.login'))

    cart_items = session.get('cart', [])

    valid_cart_items = []
    for product_id in cart_items:
        if product_id in products_dict:
            valid_cart_items.append(product_id)

    if len(valid_cart_items) != len(cart_items):
        session['cart'] = valid_cart_items
        session.modified = True

    unread_notifications = get_unread_notifications(session.get('username'))

    return render_template(
        "dashboard/cart.html",
        current_user=current_user,
        cart_items=valid_cart_items,
        products_dict=products_dict,
        unread_notifications=unread_notifications
    )


@dashboard_bp.route('/add', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        flash('Трябва да сте влезли в системата', 'warning')
        return redirect(url_for('auth.login'))

    product_id = request.form.get('product_id')

    if 'cart' not in session:
        session['cart'] = []

    if product_id in products_dict:
        product = products_dict[product_id]
        if product.in_stock > 0:
            session['cart'].append(product_id)
            session.modified = True
            flash(f'{product.name} е добавен в количката!', 'success')
        else:
            flash('Продуктът е изчерпан!', 'warning')
    else:
        flash('Продуктът не е намерен!', 'error')

    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/clear_cart')
def clear_cart():
    if 'cart' in session:
        session['cart'] = []
        session.modified = True
        flash('Количката е изчистена!', 'success')
    return redirect(url_for('dashboard.cart_page'))


@dashboard_bp.route('/admin')
def admin():
    if 'username' not in session:
        flash('Моля, влезте в системата.', 'warning')
        return redirect(url_for('auth.login'))

    if session['username'] != 'admin':
        flash('Нямате права за достъп до административния панел.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    users_count = len(accounts)
    products_count = len(all_products)
    orders_count = len(orders)
    total_revenue = sum(order.get('total', 0) for order in orders)

    current_user.username = session['username']

    return render_template(
        'dashboard/admin.html',
        current_user=current_user,
        users_count=users_count,
        products_count=products_count,
        orders_count=orders_count,
        total_revenue=total_revenue,
        users=accounts,
        orders=orders,
        products=all_products
    )


@dashboard_bp.route('/admin/add_product', methods=['POST'])
def add_product():
    if 'username' not in session or session['username'] != 'admin':
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    name = request.form.get('name')
    category = request.form.get('category')
    price = float(request.form.get('price'))
    stock = int(request.form.get('stock'))

    try:
        product_id = add_new_product(name, category, price, stock)
        add_product_notification(name, category, price)
        flash(f'Продукт "{name}" е добавен успешно!', 'success')
    except Exception as e:
        flash(f'Грешка при добавяне на продукт: {str(e)}', 'error')

    return redirect(url_for('dashboard.admin'))


@dashboard_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'username' not in session:
        flash('Трябва да сте влезли в системата', 'warning')
        return redirect(url_for('auth.login'))

    product_id = request.form.get('product_id')

    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        session.modified = True
        flash('Продуктът е премахнат от количката!', 'success')

    return redirect(url_for('dashboard.cart_page'))


@dashboard_bp.route('/admin/delete_user/<username>')
def delete_user(username):
    if 'username' not in session or session['username'] != 'admin':
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    if username == 'admin':
        flash('Не можете да изтриете администраторския акаунт.', 'error')
        return redirect(url_for('dashboard.admin'))

    global accounts
    accounts = [user for user in accounts if user[0] != username]
    flash(f'Потребител {username} е изтрит успешно!', 'success')
    return redirect(url_for('dashboard.admin'))


@dashboard_bp.route('/admin/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    if 'username' not in session or session['username'] != 'admin':
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    if 0 < order_id <= len(orders):
        deleted_order = orders.pop(order_id - 1)
        flash(f'Поръчка #{order_id} е изтрита успешно!', 'success')
    else:
        flash('Поръчката не е намерена.', 'error')

    return redirect(url_for('dashboard.admin'))


@dashboard_bp.route('/mark_notification_read/<int:notification_id>')
def mark_notification_read(notification_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    mark_notification_as_read(notification_id, session['username'])
    return redirect(request.referrer or url_for('dashboard.dashboard'))


@dashboard_bp.route('/mark_all_notifications_read')
def mark_all_notifications_read():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    mark_all_notifications_as_read(session['username'])
    flash('Всички нотификации са маркирани като прочетени!', 'success')
    return redirect(request.referrer or url_for('dashboard.dashboard'))