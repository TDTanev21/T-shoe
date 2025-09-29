class Shoe:
    def __init__(self, name, price, in_stock, category):
        self.name = name
        self.__price = price
        self.in_stock = in_stock
        self.category = category

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError('Price cannot be negative')
        self.__price = new_price
    def get_info(self):
        return f"{self.name} - {self.category} - {self.price} лв - Налични: {self.in_stock}"

    def update_stock(self, quantity):
        self.in_stock += quantity

class SportShoe(Shoe):
    def __init__(self, name, price, in_stock):
        super().__init__(name, price, in_stock, category="Sport")

    def get_info(self):
        return f"Спортни обувки: {super().get_info()}"

class FormalShoe(Shoe):
    def __init__(self, name, price, in_stock):
        super().__init__(name, price, in_stock, category="Official")

    def get_info(self):
        return f"Официални обувки: {super().get_info()}"

class CasualShoe(Shoe):
    def __init__(self, name, price, in_stock):
        super().__init__(name, price, in_stock, category="Casual")

    def get_info(self):
        return f"Всекидневни обувки: {super().get_info()}"
