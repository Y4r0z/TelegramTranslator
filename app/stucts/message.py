from datetime import datetime
from app.stucts.channel import Channel
from app.stucts.user import User

class Message:
    def __init__(self, source : Channel, author : User, text : str, media = None):
        self.source = source
        self.author = author
        self.text = text
        self.media = media
        self.time = datetime.now()
    
    def __str__(self):
        return f'{self.author}: {self.text}'