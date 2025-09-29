from flask import render_template, session, redirect, url_for, flash, request
from auth.accounts import current_user, accounts
from . import dashboard_bp
from .orders import cart, orders, admin_products, products_dict
from .products import SportShoe, FormalShoe, CasualShoe

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Моля, влезте в системата, за да видите дашборда.', 'warning')
        return redirect(url_for('auth.login'))

    product_images = {
        'nike_air_force': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop',
        'adidas_ultraboost': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=300&fit=crop',
        'puma_rsx': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&h=300&fit=crop',
        'clarks_dress': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=300&fit=crop',
        'hugo_boss': 'https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=400&h=300&fit=crop',
        'adidas_superstar': 'https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?w=400&h=300&fit=crop',
        'new_balance_574': 'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400&h=300&fit=crop',
        'vans_old_skool': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop',
        'converse_chuck': 'https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=400&h=300&fit=crop'
    }

    current_user.username = session['username']
    return render_template('dashboard/dashboard.html',
                         current_user=current_user,
                         products_dict=products_dict,
                         product_images=product_images)  # Добави това

@dashboard_bp.route('/dashboard/cart')
def cart_page():
    cart_items = session.get('cart', [])
    return render_template(
        "dashboard/cart.html",
        current_user=current_user,
        cart_items=cart_items,
        products_dict=products_dict
    )


@dashboard_bp.route('/add', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        flash('Трябва да сте влезли в системата', 'warning')
        return redirect(url_for('auth.login'))

    product_id = request.form.get('product_id')

    if 'cart' not in session:
        session['cart'] = []

    # Проверка дали продукта съществува и има наличност
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


@dashboard_bp.route('/admin')
def admin():
    if 'username' not in session:
        flash('Моля, влезте в системата.', 'warning')
        return redirect(url_for('auth.login'))

    if session['username'] != 'admin':
        flash('Нямате права за достъп до административния панел.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    users_count = len(accounts)
    products_count = len(admin_products)
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
        products=admin_products  # Сега това са обекти от класовете
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



    if category == "Спортни":
        new_product = SportShoe(name, price, stock)
    elif category == "Елегантни":
        new_product = FormalShoe(name, price, stock)
    else:  # Всекидневни
        new_product = CasualShoe(name, price, stock)

    # Генерираме уникален ID
    product_id = name.lower().replace(' ', '_')

    # Добавяме в списъците
    admin_products.append(new_product)
    products_dict[product_id] = new_product

    flash(f'Продукт "{name}" е добавен успешно!', 'success')
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

    # Не позволявай изтриване на администратора
    if username == 'admin':
        flash('Не можете да изтриете администраторския акаунт.', 'error')
        return redirect(url_for('dashboard.admin'))

    # Изтриване на потребителя от accounts списъка
    global accounts
    accounts = [user for user in accounts if user[0] != username]

    flash(f'Потребител {username} е изтрит успешно!', 'success')
    return redirect(url_for('dashboard.admin'))


@dashboard_bp.route('/admin/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    if 'username' not in session or session['username'] != 'admin':
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    from .orders import orders
    if 0 < order_id <= len(orders):
        deleted_order = orders.pop(order_id - 1)
        flash(f'Поръчка #{order_id} е изтрита успешно!', 'success')
    else:
        flash('Поръчката не е намерена.', 'error')

    return redirect(url_for('dashboard.admin'))