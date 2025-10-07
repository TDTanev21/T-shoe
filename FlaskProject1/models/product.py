from . import db


class Shoe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50), default="Общи")
    brand = db.Column(db.String(50), default="Други")
    color = db.Column(db.String(30), default="Черен")
    size = db.Column(db.String(10), default="42")
    shoe_type = db.Column(db.String(20))
    __mapper_args__ = {
        'polymorphic_identity': 'shoe',
        'polymorphic_on': shoe_type
    }

    def get_info(self):
        return f"{self.brand} {self.name} - {self.color} - Размер: {self.size}"

    def matches_search(self, search_term):
        search_term = search_term.lower()
        return (search_term in self.name.lower() or
                search_term in self.brand.lower() or
                search_term in self.category.lower() or
                search_term in self.subcategory.lower())


class SportShoe(Shoe):
    id = db.Column(db.Integer, db.ForeignKey('shoe.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'sport_shoe',
    }

    def get_info(self):
        return f"{self.subcategory}: {super().get_info()}"


class FormalShoe(Shoe):
    id = db.Column(db.Integer, db.ForeignKey('shoe.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'formal_shoe',
    }

    def get_info(self):
        return f"{self.subcategory}: {super().get_info()}"


class CasualShoe(Shoe):
    id = db.Column(db.Integer, db.ForeignKey('shoe.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'casual_shoe',
    }

    def get_info(self):
        return f"{self.subcategory}: {super().get_info()}"