from models.product import SportShoe, FormalShoe, CasualShoe

# Инициализация на продукти
sport_shoe1 = SportShoe("Air Force 1", 199.99, 15, "Баскетбол", "Nike", "Бял", "42")
sport_shoe2 = SportShoe("Ultraboost", 229.99, 8, "Бягане", "Adidas", "Черен", "43")
sport_shoe3 = SportShoe("RS-X", 159.99, 12, "Тренировка", "Puma", "Син", "41")
sport_shoe4 = SportShoe("Predator", 299.99, 6, "Футбол", "Adidas", "Червен", "44")
sport_shoe5 = SportShoe("Air Max", 179.99, 10, "Бягане", "Nike", "Сив", "42")

formal_shoe1 = FormalShoe("Oxford", 279.99, 5, "Оксфорди", "Clarks", "Кафяв", "43")
formal_shoe2 = FormalShoe("Boss Classic", 399.99, 3, "Лофери", "Hugo Boss", "Черен", "44")
formal_shoe3 = FormalShoe("Derby", 249.99, 7, "Дърбита", "Geox", "Черен", "42")
formal_shoe4 = FormalShoe("Monk Strap", 329.99, 4, "Монкстрапове", "Salvatore", "Кафяв", "43")

casual_shoe1 = CasualShoe("Superstar", 179.99, 10, "Кецове", "Adidas", "Бял", "42")
casual_shoe2 = CasualShoe("574", 169.99, 7, "Кецове", "New Balance", "Сив", "43")
casual_shoe3 = CasualShoe("Old Skool", 129.99, 20, "Кецове", "Vans", "Черен", "41")
casual_shoe4 = CasualShoe("Chuck 70", 149.99, 15, "Кецове", "Converse", "Червен", "42")
casual_shoe5 = CasualShoe("Desert Boot", 189.99, 8, "Ботуши", "Clarks", "Бежов", "43")

all_products = [
    sport_shoe1, sport_shoe2, sport_shoe3, sport_shoe4, sport_shoe5,
    formal_shoe1, formal_shoe2, formal_shoe3, formal_shoe4,
    casual_shoe1, casual_shoe2, casual_shoe3, casual_shoe4, casual_shoe5
]

products_dict = {}
for i, product in enumerate(all_products):
    product_id = f"{product.brand.lower()}_{product.name.lower().replace(' ', '_')}_{i}"
    products_dict[product_id] = product

CATEGORIES = {
    "Спортни": ["Бягане", "Баскетбол", "Футбол", "Тенис", "Тренировка", "Волейбол"],
    "Елегантни": ["Оксфорди", "Дърбита", "Лофери", "Монкстрапове", "Брогове"],
    "Всекидневни": ["Кецове", "Мокасини", "Ботуши", "Сандали", "Еспадрили"]
}

BRANDS = ["Nike", "Adidas", "Puma", "New Balance", "Vans", "Converse", "Clarks", "Hugo Boss", "Geox", "Salvatore"]

orders = [
    {
        'user': 'user1',
        'products': ['adidas_ultraboost_1', 'nike_air_force_1_0'],
        'total': 429.98,
        'status': 'изпълнена'
    }
]

cart = []