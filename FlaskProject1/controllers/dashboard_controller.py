from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.product import Shoe
from models.user import User
from models.order import Order, OrderItem
from models import db
from services.product_service import get_filtered_products, add_new_product
from models.review import Review
dashboard_bp = Blueprint('dashboard', __name__)
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

CATEGORIES = {
    "Спортни": ["Бягане", "Баскетбол", "Футбол", "Тенис", "Тренировка", "Волейбол"],
    "Елегантни": ["Оксфорди", "Дърбита", "Лофери", "Монкстрапове", "Брогове"],
    "Всекидневни": ["Кецове", "Мокасини", "Ботуши", "Сандали", "Еспадрили"]
}

BRANDS = ["Nike", "Adidas", "Puma", "New Balance", "Vans", "Converse", "Clarks", "Hugo Boss", "Geox", "Salvatore"]

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
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
                           max_price=max_price)


@dashboard_bp.route('/dashboard/cart')
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
        products_dict=products_dict
    )


@dashboard_bp.route('/add', methods=['POST'])
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


@dashboard_bp.route('/clear_cart')
@login_required
def clear_cart():
    if 'cart' in session:
        session['cart'] = []
        session.modified = True
        flash('Количката е изчистена!', 'success')
    return redirect(url_for('dashboard.cart_page'))


@dashboard_bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Нямате права за достъп до административния панел.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    users_count = User.query.count()
    products_count = Shoe.query.count()
    orders_count = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total)).scalar() or 0

    users = User.query.all()
    orders = Order.query.all()
    products = Shoe.query.all()

    return render_template(
        'dashboard/admin.html',
        current_user=current_user,
        users_count=users_count,
        products_count=products_count,
        orders_count=orders_count,
        total_revenue=total_revenue,
        users=users,
        orders=orders,
        products=products
    )


@dashboard_bp.route('/admin/add_product', methods=['POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    name = request.form.get('name')
    category = request.form.get('category')
    price = request.form.get('price')
    stock = request.form.get('stock')

    if not all([name, category, price, stock]):
        flash('Моля, попълнете всички полета.', 'error')
        return redirect(url_for('dashboard.admin'))

    try:
        price = float(price)
        stock = int(stock)
        if price < 0 or stock < 0:
            raise ValueError
    except ValueError:
        flash('Невалидни данни за цена или наличност.', 'error')
        return redirect(url_for('dashboard.admin'))

    try:
        product_id = add_new_product(name, category, price, stock)
        flash(f'Продукт "{name}" е добавен успешно!', 'success')
    except Exception as e:
        flash(f'Грешка при добавяне на продукт: {str(e)}', 'error')

    return redirect(url_for('dashboard.admin'))
@dashboard_bp.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    user = User.query.get(user_id)
    if not user:
        flash('Потребителят не е намерен.', 'error')
        return redirect(url_for('dashboard.admin'))

    if user.id == current_user.id:
        flash('Не можете да изтриете собствения си акаунт.', 'error')
        return redirect(url_for('dashboard.admin'))

    try:
        Order.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        flash(f'Потребител {user.username} е изтрит успешно!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Грешка при изтриване на потребител: {str(e)}', 'error')

    return redirect(url_for('dashboard.admin'))


@dashboard_bp.route('/admin/delete_order/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    if not current_user.is_admin:
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    order = Order.query.get(order_id)
    if not order:
        flash('Поръчката не е намерена.', 'error')
        return redirect(url_for('dashboard.admin'))

    try:
        for item in order.items:
            product = Shoe.query.get(item.product_id)
            if product:
                product.in_stock += item.quantity

        db.session.delete(order)
        db.session.commit()
        flash(f'Поръчка #{order_id} е изтрита успешно!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Грешка при изтриване на поръчка: {str(e)}', 'error')

    return redirect(url_for('dashboard.admin'))


@dashboard_bp.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash('Нямате права за тази операция.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    product = Shoe.query.get(product_id)
    if not product:
        flash('Продуктът не е намерен.', 'error')
        return redirect(url_for('dashboard.admin'))

    try:
        order_items = OrderItem.query.filter_by(product_id=product_id).first()
        if order_items:
            flash('Не можете да изтриете продукт, който е част от активни поръчки.', 'error')
            return redirect(url_for('dashboard.admin'))

        db.session.delete(product)
        db.session.commit()
        flash(f'Продукт "{product.name}" е изтрит успешно!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Грешка при изтриване на продукт: {str(e)}', 'error')

    return redirect(url_for('dashboard.admin'))


@dashboard_bp.route('/see_product/<product_id>')
@login_required
def see_product(product_id):
    try:
        # Вземане на продукта от базата данни
        product_db_id = int(product_id.split('_')[-1])
        product = Shoe.query.get(product_db_id)

        if not product:
            flash('Продуктът не е намерен.', 'error')
            return redirect(url_for('dashboard.dashboard'))

        # Генериране на product_id за снимката
        base_key = product_id.rsplit('_', 1)[0]
        product_image = PRODUCT_IMAGES.get(base_key, 'default.png')
        reviews = Review.query.filter_by(product_id=product_db_id).all()

        average_rating = 0
        if reviews:
            average_rating = sum(review.rating for review in reviews) / len(reviews)

        user_review = None
        if current_user.is_authenticated:
            user_review = Review.query.filter_by(
                product_id=product_db_id,
                user_id=current_user.id
            ).first()

        return render_template('dashboard/product.html',
                               product=product,
                               product_id=product_id,
                               product_image=product_image,
                               current_user=current_user,
                               reviews=reviews,
                               average_rating=round(average_rating, 1),
                               total_reviews=len(reviews),
                               user_review=user_review)

    except (ValueError, IndexError) as e:
        flash('Невалиден продукт.', 'error')
        return redirect(url_for('dashboard.dashboard'))