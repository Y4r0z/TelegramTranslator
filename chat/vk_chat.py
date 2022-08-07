from vkbottle import API
from chat.chat import Chat
from data_manager import DataManager
import platforms
class VkChat(Chat):
    Platform = platforms.Platform.vkontakte
    def __init__(self, chat, peer_id):
        super().__init__(peer_id, chat.chat_settings.title, chat)
        self.subscriptions = []

    @staticmethod
    async def FromId(api : API, peer_id):
        chat = await api.messages.get_conversations_by_id(peer_ids=[peer_id])
        return VkChat(chat.items[0], peer_id)
    
    def isSubscribedTo(self, chatId : int):
        flag = False
        for i in self.subscriptions:
            if DataManager().cmpTgId(i.id, chatId):
                flag = True
        return flag
    
    def toDict(self):
        return {'name':self.name, 'id':self.id, 'subscriptions':[i.toDict() for i in self.subscriptions]}
