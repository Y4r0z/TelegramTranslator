from messages.media import Media, MediaType
from datetime import datetime as dt
class Message:
    def __init__(self, channel : str, author : str, text : str, media : Media = None):
        self.channel = channel
        self.author = author
        self.text = text
        self.time = dt.now()
        self.media : Media = media
    
    def __str__(self):
        return f'{self.channel} - {self.author}: {"".join(self.text[0:24])}'
    
    @staticmethod
    def TimeDiff(mes1, mes2):
        diff = (mes1.time - mes2.time).total_seconds()
        return abs(diff)