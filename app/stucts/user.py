class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def __str__(self):
        return f'{self.name}#{self.id}'