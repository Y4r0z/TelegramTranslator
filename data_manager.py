from telethon import TelegramClient, utils
class DataManager:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DataManager, cls).__new__(cls)
            cls.__instance.__init()
        return cls.__instance
    
    def __init(self):
        self.allTgChats = []
        self.vkChats = []
        self.tgChats = []
    
    
    def tg_findById(self, peer_id):
        flag = False
        for i in self.tgChats:
            if self.cmpTgId(i.id, peer_id):
                flag = True
        return flag
    
    def vk_findById(self, peer_id):
        flag = False
        for i in self.vkChats:
            if i.id == peer_id:
                flag = True
        return flag
    
    def tg_getById(self, peer_id):
        for i in self.tgChats:
            if self.cmpTgId(i.id, peer_id):
                return i
        return None
    
    def vk_getById(self, peer_id):
        for i in self.vkChats:
            if i.id == peer_id:
                return i
        return None
    
    async def tg_getEntityByName(self, bot : TelegramClient, name):
        chat = None
        try:
            chat = await bot.get_entity(name)
        except Exception as e:
            print('tg_getEntityByName не удалось получить энтити.', e)
        return chat
    
    def cmpTgId(self, id1, id2):
        return abs(id1) == abs(id2) or -1000000000000 - id1 == id2 or -1000000000000 + id1 == id2\
            or -1000000000000 - id2 == id1 or -1000000000000 + id2 == id1

