from app.structs.object.object import Object

class User(Object):
    def __init__(self, name, _id):
        super().__init__(name, _id)
    
    @staticmethod
    def FromJson(json):
        return User(json['name'], int(json['id']))