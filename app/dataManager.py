from app.structs.object.channel import Channel
from app.filemanager import FileManager
from app.structs.object.user import User
from app.structs.message import Message

class DataManager:
    _instance = None
    def __new__(self):
        if self._instance is None:
            self._instance = super().__new__(self)
            self.fm = FileManager()
            self.tgChats : list[Channel] = [Channel.FromJson(i) for i in self.fm.loadChats()]
            self.tgHistory : list[Message] = []
            self.vkHistory : list[Message] = []
        return self._instance
    
    def subscribe(self, tgChat : str, vkChat : Channel):
        for i in self.tgChats:
            if i.strEqual(tgChat):
                i.append(vkChat)
                return True
        return False
    
    def unsubscribe(self, tgChat : str, vkChat : Channel):
        for i in self.tgChats:
            if not i.strEqual(tgChat):
                continue
            for j in range(len(i.subscribers)):
                if i.subscribers[j].id != vkChat.id:
                    continue
                i.subscribers.pop(j)
                return True
        return False

    async def saveMedia(self, mes):
        await self.fm.saveMedia(mes)
    
    def save(self):
        self.fm.saveChats(self.tgChats)

    def exit(self):
        self.save()