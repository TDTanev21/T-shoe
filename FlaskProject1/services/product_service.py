from models.product import Shoe, SportShoe, FormalShoe, CasualShoe
from models import db

def get_filtered_products(search_term="", category_filter="", subcategory_filter="",
                          brand_filter="", min_price="", max_price=""):
    query = Shoe.query

    if search_term:
        query = query.filter(
            db.or_(
                Shoe.name.ilike(f'%{search_term}%'),
                Shoe.brand.ilike(f'%{search_term}%'),
                Shoe.category.ilike(f'%{search_term}%'),
                Shoe.subcategory.ilike(f'%{search_term}%')
            )
        )

    if category_filter:
        query = query.filter(Shoe.category == category_filter)

    if subcategory_filter:
        query = query.filter(Shoe.subcategory == subcategory_filter)

    if brand_filter:
        query = query.filter(Shoe.brand == brand_filter)

    if min_price:
        try:
            query = query.filter(Shoe.price >= float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            query = query.filter(Shoe.price <= float(max_price))
        except ValueError:
            pass

    return {f"{shoe.brand.lower()}_{shoe.name.lower().replace(' ', '_')}_{shoe.id}": shoe
            for shoe in query.all()}


def add_new_product(name, category, price, stock, subcategory="Общи", brand="Други", color="Черен", size="42"):
    if category == "Спортни":
        new_product = SportShoe(
            name=name, price=price, in_stock=stock,
            category=category, subcategory=subcategory,
            brand=brand, color=color, size=size
        )
    elif category == "Елегантни":
        new_product = FormalShoe(
            name=name, price=price, in_stock=stock,
            category=category, subcategory=subcategory,
            brand=brand, color=color, size=size
        )
    else:
        new_product = CasualShoe(
            name=name, price=price, in_stock=stock,
            category=category, subcategory=subcategory,
            brand=brand, color=color, size=size
        )

    db.session.add(new_product)
    db.session.commit()

    return f"{new_product.brand.lower()}_{new_product.name.lower().replace(' ', '_')}_{new_product.id}"