
class Channel:
    def __init__(self, name, _id):
        self.name = name
        self.id = _id
    
    def __str__(self):
        return f'{self.name}#{self.id}'