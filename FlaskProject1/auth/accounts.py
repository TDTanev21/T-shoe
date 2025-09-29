accounts = [
    ('t', 't'),
    ('admin', 'admin'),
]

class User:
    def __init__(self):
        self.username = None
        self.is_authenticated = False

current_user = User()