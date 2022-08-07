from telethon import utils
from chat.chat import Chat
import platforms
class TelegramChat(Chat):
    Platform = platforms.Platform.telegram

    def __init__(self, chat, name, _id):
        super().__init__(_id, name, chat)


    @staticmethod
    async def FromName(bot, name : str):
        chat = None
        dialogs = await bot.get_dialogs()
        for i in dialogs:
            if name.lower() != i.name.lower(): continue
            chat = i
        if chat is None:
            raise Exception("Не получилось найти канал по названию.")
            return None
        return TelegramChat(chat, chat.name, chat.id)
    
    @staticmethod
    async def FromId(bot, peer_id : int):
        chat = None
        dialogs = await bot.get_dialogs()
        for i in dialogs:
            if abs(peer_id) != abs(i.id) and -1000000000000 - peer_id != i.id and -1000000000000 + peer_id != i.id: continue
            chat = i
        if chat is None:
            raise Exception("Не получилось найти канал по ID.")
            return None
        return TelegramChat(chat, chat.name, chat.id)

    @staticmethod
    async def FromAny(bot, other):
        if isinstance(other, int):
            return await TelegramChat.FromId(bot, other)
        elif other.isnumeric():
            return await TelegramChat.FromId(bot, int(other))
        elif isinstance(other, str):
            return await TelegramChat.FromName(bot, other)
        else:
            raise Exception("TelegramChat.FromAny - неправильный тип!.")
            return None

    