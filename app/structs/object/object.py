class Object:
    def __init__(self, name, _id):
        self.name = name
        self.id = _id
    
    def __str__(self):
        return f'{self.name}#{self.id}'
    
    def __eq__(self, o):
        return self.id == o.id

    def strEqual(self, o):
        cmp = str(o)
        return cmp == str(self.id) or cmp == self.name or cmp ==  f'{self.name}#{self.id}' or cmp ==  f'#{self.id}'
    
    def json(self):
        return {'name':self.name, 'id':self.id}