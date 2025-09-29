from .products import SportShoe, FormalShoe, CasualShoe

# Създаваме инстанции на обувките
sport_shoe1 = SportShoe("Nike Air Force 1", 199.99, 15)
sport_shoe2 = SportShoe("Adidas Ultraboost", 229.99, 8)
sport_shoe3 = SportShoe("Puma RS-X", 159.99, 12)

formal_shoe1 = FormalShoe("Clarks Dress Shoes", 279.99, 5)
formal_shoe2 = FormalShoe("Hugo Boss Оксфорди", 399.99, 3)

casual_shoe1 = CasualShoe("Adidas Superstar", 179.99, 10)
casual_shoe2 = CasualShoe("New Balance 574", 169.99, 7)
casual_shoe3 = CasualShoe("Vans Old Skool", 129.99, 20)
casual_shoe4 = CasualShoe("Converse Chuck 70", 149.99, 15)

# Списък с всички продукти за администраторски панел
admin_products = [
    sport_shoe1, sport_shoe2, sport_shoe3,
    formal_shoe1, formal_shoe2,
    casual_shoe1, casual_shoe2, casual_shoe3, casual_shoe4
]

# Речник за бърз достъп по ID (за количката)
products_dict = {
    'nike_air_force': sport_shoe1,
    'adidas_ultraboost': sport_shoe2,
    'puma_rsx': sport_shoe3,
    'clarks_dress': formal_shoe1,
    'hugo_boss': formal_shoe2,
    'adidas_superstar': casual_shoe1,
    'new_balance_574': casual_shoe2,
    'vans_old_skool': casual_shoe3,
    'converse_chuck': casual_shoe4
}

# Примерни данни за поръчки
orders = [
    {
        'user': 'user1',
        'products': ['nike_air_force', 'adidas_ultraboost'],
        'total': 429.98,
        'status': 'изпълнена'
    },
    {
        'user': 'user2', 
        'products': ['converse_chuck'],
        'total': 149.99,
        'status': 'обработва се'
    }
]

cart = []