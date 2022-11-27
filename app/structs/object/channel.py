from app.structs.object.object import Object

class Channel(Object):
    def __init__(self, name, _id):
        super().__init__(name, _id)
        self.subscribers = []
    
    def append(self, o):
        if o not in self.subscribers:
            self.subscribers.append(o)