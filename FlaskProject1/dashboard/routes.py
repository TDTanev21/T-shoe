from flask import render_template, session, redirect, url_for, flash, request
from auth.accounts import current_user, accounts
from . import dashboard_bp
from .orders import cart, orders, admin_products  # Добави admin_products


@dashboard_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Моля, влезте в системата, за да видите дашборда.', 'warning')
        return redirect(url_for('auth.login'))

    current_user.username = session['username']
    return render_template('dashboard/dashboard.html', current_user=current_user)


@dashboard_bp.route('/dashboard/cart')
def cart_page():
    print("DEBUG: Session data:", dict(session))
    print("DEBUG: Cart in session:", session.get('cart'))

    cart_items = session.get('cart', [])
    print("DEBUG: Cart items:", cart_items)

    return render_template(
        "dashboard/cart.html",
        current_user=current_user,
        cart_items=cart_items
    )


@dashboard_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        flash('Трябва да сте влезли в системата', 'warning')
        return redirect(url_for('auth.login'))

    product_id = request.form.get('product_id')
    print(f"DEBUG: Adding product {product_id} to cart")
    print(f"DEBUG: Session before: {dict(session)}")

    # Инициализиране на количката, ако не съществува
    if 'cart' not in session:
        session['cart'] = []
        print("DEBUG: Created new cart in session")

    # Добавяне на продукта
    session['cart'].append(product_id)
    session.modified = True  # Важно: маркиране на сесията като променена

    print(f"DEBUG: Cart after add: {session['cart']}")
    print(f"DEBUG: Session after: {dict(session)}")

    flash('Продуктът е добавен в количката!', 'success')
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
    products_count = len(admin_products)  # Сега използваме реалния брой
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
        products=admin_products  # Добави продуктите за показване в таблицата
    )


@dashboard_bp.route('/admin/add_product', methods=['POST'])
def add_product():
    if 'username' not in session or session['username'] != 'admin':
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    name = request.form.get('name')
    category = request.form.get('category')
    price = request.form.get('price')
    stock = request.form.get('stock')

    # Добавяне на нов продукт в списъка
    new_product = {
        'name': name,
        'category': category,
        'price': float(price),
        'stock': int(stock)
    }

    from .orders import admin_products
    admin_products.append(new_product)

    flash(f'Продукт "{name}" е добавен успешно!', 'success')
    return redirect(url_for('dashboard.admin'))


@dashboard_bp.route('/admin/delete_order/<int:order_id>')
def delete_order(order_id):
    if 'username' not in session or session['username'] != 'admin':
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    # Изтриване на поръчка (проста версия)
    if 0 < order_id <= len(orders):
        deleted_order = orders.pop(order_id - 1)
        flash(f'Поръчка #{order_id} е изтрита успешно!', 'success')
    else:
        flash('Поръчката не е намерена.', 'error')

    return redirect(url_for('dashboard.admin'))


#@dashboard_bp.route('/admin/delete_user/<username>')
#def delete_user(username):
#    if 'username' not in session or session['username'] != 'admin':
#        flash('Нямате права за тази операция.', 'error')
#        return redirect(url_for('dashboard.dashboard'))
#
#    if username == session['username']:
#        flash('Не можете да изтриете собствения си акаунт!', 'error')
#        return redirect(url_for('dashboard.admin'))
#
#    user_exists = any(user[0] == username for user in accounts)
#
#    if user_exists:
#        global accounts
#        accounts = [user for user in accounts if user[0] != username]
#        flash(f'Потребител "{username}" е изтрит успешно!', 'success')
#    else:
#        flash('Потребителят не е намерен.', 'error')
#
#    return redirect(url_for('dashboard.admin'))
@dashboard_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'username' not in session:
        flash('Трябва да сте влезли в системата', 'warning')
        return redirect(url_for('auth.login'))

    product_id = request.form.get('product_id')
    print(f"DEBUG: Removing product {product_id} from cart")

    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        session.modified = True
        flash('Продуктът е премахнат от количката!', 'success')
        print(f"DEBUG: Cart after remove: {session.get('cart', [])}")

    return redirect(url_for('dashboard.cart_page'))