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

# Добави този речник за колички на потребителите
user_carts = {}  # {username: [product_ids]}