from datetime import datetime
from app.structs.object.channel import Channel
from app.structs.object.user import User

class Message:
    def __init__(self, source : Channel, author : User, text : str, media = None, _id = None):
        self.id = _id
        self.source = source
        self.author = author
        self.text = text
        self.media = media
        self.time = datetime.now()
    
    def __str__(self):
        return f'{self.author}: {self.text}'