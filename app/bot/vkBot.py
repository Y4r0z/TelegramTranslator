from vkbottle.bot import Bot, Message, Blueprint
from vkbottle.tools import DocMessagesUploader, PhotoMessageUploader, AudioUploader, VideoUploader, VoiceMessageUploader
import asyncio
from asyncio import AbstractEventLoop

from app.bot.bot import ChatBot

from app.structs.message import Message as MyMessage
from app.structs.object.channel import Channel as MyChannel
from app.structs.object.user import User as MyUser


class VkBot(ChatBot):

    def __init__(self, api : str, loop : AbstractEventLoop):
        super().__init__() 
        self.loop = loop
        self.bot = Bot(api, loop = self.loop)

        @self.bot.on.message()
        async def messageHandler(message : Message):
            text = message.text      
            if len(text) <= 0: return
            userId = message.from_id
            chatId = message.chat_id
            userInfo = await self.bot.api.users.get(userId)
            userName = f"{userInfo[0].first_name} {userInfo[0].last_name}"
            #chatInfo = await self.bot.api.messages.get_conversations_by_id(chatId)
            chatName = "VK"
            user = MyUser(userName, userId)
            chat = MyChannel(chatName, chatId)
            self.newMessage.emit(MyMessage(chat, user, text))
          