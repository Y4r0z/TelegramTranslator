from app.structs.object.object import Object
from app.structs.object.user import User

class Channel(Object):
    def __init__(self, name, _id):
        super().__init__(name, _id)
        self.subscribers : list[Channel] = []
    
    def append(self, o):
        if o not in self.subscribers:
            self.subscribers.append(o)
    
    def json(self):
        return {
            'name': self.name,
            'id': self.id,
            'subscribers': [i.json() for i in self.subscribers]
        }
    
    @staticmethod
    def FromJson(json):
        ch = Channel(json['name'], int(json['id']))
        ch.subscribers = [User.FromJson(i) for i in json['subscribers']]
        return ch