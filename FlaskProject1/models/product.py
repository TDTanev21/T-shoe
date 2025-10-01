class Shoe:
    def __init__(self, name, price, in_stock, category, subcategory="Общи", brand="Други", color="Черен", size="42"):
        self.name = name
        self.__price = price
        self.in_stock = in_stock
        self.category = category
        self.subcategory = subcategory
        self.brand = brand
        self.color = color
        self.size = size

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError('Price cannot be negative')
        self.__price = new_price

    def get_info(self):
        return f"{self.brand} {self.name} - {self.color} - Размер: {self.size}"

    def update_stock(self, quantity):
        self.in_stock += quantity

    def matches_search(self, search_term):
        search_term = search_term.lower()
        return (search_term in self.name.lower() or
                search_term in self.brand.lower() or
                search_term in self.category.lower() or
                search_term in self.subcategory.lower())

class SportShoe(Shoe):
    def __init__(self, name, price, in_stock, subcategory="Тениски", brand="Nike", color="Бял", size="42"):
        super().__init__(name, price, in_stock, "Спортни", subcategory, brand, color, size)

    def get_info(self):
        return f"{self.subcategory}: {super().get_info()}"

class FormalShoe(Shoe):
    def __init__(self, name, price, in_stock, subcategory="Оксфорди", brand="Clarks", color="Черен", size="42"):
        super().__init__(name, price, in_stock, "Елегантни", subcategory, brand, color, size)

    def get_info(self):
        return f"{self.subcategory}: {super().get_info()}"

class CasualShoe(Shoe):
    def __init__(self, name, price, in_stock, subcategory="Кецове", brand="Adidas", color="Син", size="42"):
        super().__init__(name, price, in_stock, "Всекидневни", subcategory, brand, color, size)

    def get_info(self):
        return f"{self.subcategory}: {super().get_info()}"