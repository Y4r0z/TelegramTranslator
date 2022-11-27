from app.structs.object.channel import Channel

class DataManager:
    def __init__(self):
        self.tgChats = []
    
    def subscribe(self, tgChat : str, vkChat : Channel):
        for i in self.tgChats:
            if i.strEqual(tgChat):
                i.append(vkChat)
                return True
        return False
    
    def unsubscribe(self, tgChat : str, vkChat : Channel):
        for i in range(0, len(self.tgChats)):
            if self.tgChats[i].strEqual(tgChat):
                self.tgChats.pop(i)
                return True
            return False
