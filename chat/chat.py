import platforms
class Chat:
    Platform = platforms.Platform.none
    def __init__(self, _id, name, chatObject):
        self.id = _id
        self.name = name
        self.chat = chatObject
    def __eq__(self, o):
        return self.id == o.id

    def __ne__(self, o):
        return self.id != o.id
    
    def __str__(self):
        return f'{self.name}#{self.id}'
    
    def toDict(self):
        return {'name':self.name, 'id':self.id}