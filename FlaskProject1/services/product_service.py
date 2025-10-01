from models.order import products_dict, all_products
from models.product import SportShoe, FormalShoe, CasualShoe


def get_filtered_products(search_term="", category_filter="", subcategory_filter="",
                          brand_filter="", min_price="", max_price=""):
    filtered_products = {}

    for product_id, product in products_dict.items():
        if search_term and not product.matches_search(search_term):
            continue

        if category_filter and product.category != category_filter:
            continue

        if subcategory_filter and product.subcategory != subcategory_filter:
            continue

        if brand_filter and product.brand != brand_filter:
            continue

        if min_price:
            try:
                if product.price < float(min_price):
                    continue
            except ValueError:
                pass

        if max_price:
            try:
                if product.price > float(max_price):
                    continue
            except ValueError:
                pass

        filtered_products[product_id] = product

    return filtered_products


def add_new_product(name, category, price, stock):
    if category == "Спортни":
        new_product = SportShoe(name, price, stock)
    elif category == "Елегантни":
        new_product = FormalShoe(name, price, stock)
    else:
        new_product = CasualShoe(name, price, stock)

    product_id = name.lower().replace(' ', '_') + f"_{len(products_dict)}"

    all_products.append(new_product)
    products_dict[product_id] = new_product

    return product_id