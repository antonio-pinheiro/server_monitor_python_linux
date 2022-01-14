class Server:
    def __init__(self, name, ip_address, category, id=None):
        self.id = id
        self.name = name
        self.ip_address = ip_address
        self.category = category

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password