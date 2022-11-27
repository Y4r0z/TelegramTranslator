from vkbottle.bot import Bot, Message, Blueprint
from vkbottle.tools import DocMessagesUploader, PhotoMessageUploader, AudioUploader, VideoUploader, VoiceMessageUploader
import asyncio
from asyncio import AbstractEventLoop

from app.bot.bot import ChatBot

class VkBot(ChatBot):

    def __init__(self, api : str, loop : AbstractEventLoop):
        super().__init__() 
        self.loop = loop
        self.bot = Bot(api, loop = self.loop)

        @self.bot.on.message()
        async def messageHandler(message : Message):
            text = message.text
            if len(text) <= 0:
                return
            if text[0] == '/':
                self.newCommand.emit(text[1:])
            else:
                self.newMessage.emit(text)
        
        self.loop.create_task(self.bot.run_polling())
