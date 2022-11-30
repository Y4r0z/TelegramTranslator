from vkbottle.bot import Bot, Message, Blueprint
from vkbottle.tools import DocMessagesUploader, PhotoMessageUploader, AudioUploader, VideoUploader, VoiceMessageUploader
import asyncio
from asyncio import AbstractEventLoop
from app.bot.bot import ChatBot
from app.structs.message import Message as MyMessage
from app.structs.object.channel import Channel as MyChannel
from app.structs.object.user import User as MyUser
from app.dataManager import  DataManager
import random
import os
import logging as log

class VkBot(ChatBot):

    def __init__(self, api : str, loop : AbstractEventLoop):
        super().__init__() 
        self.loop = loop
        self.bot = Bot(api, loop = self.loop)

        @self.bot.on.message()
        async def messageHandler(message : Message):
            _id = message.get_message_id()
            text = message.text      
            if len(text) <= 0: return
            userId = message.from_id
            chatId = 2000000000 + message.chat_id
            userInfo = await self.bot.api.users.get(userId)
            userName = f"{userInfo[0].first_name} {userInfo[0].last_name}"
            #chatInfo = await self.bot.api.messages.get_conversations_by_id(chatId)
            chatName = "VK"
            user = MyUser(userName, userId)
            chat = MyChannel(chatName, chatId)
            self.newMessage.emit(MyMessage(chat, user, text, _id = _id, message=message))
        
    async def sendMessage(self, chatId, message : MyMessage):
        media = await DataManager().fm.saveMedia(message)
        f = None
        if media is not None:
            try:
                if message.media.audio or message.media.voice:
                    f = await VoiceMessageUploader(self.bot.api).upload(media.split('/')[-1], media, peer_id=chatId)
                elif message.media.photo:
                    f = await PhotoMessageUploader(self.bot.api).upload(media, peer_id = chatId)
                else:
                    f = await DocMessagesUploader(self.bot.api).upload(media.split('/')[-1], media, peer_id=chatId)
            except Exception as e:
                log.error('Не удалось отправить медиа: ' + str(e))
                f = None
        await self.bot.api.messages.send(
            random_id = random.getrandbits(64),
            peer_id = chatId, 
            message =  '<Пусто>' if not message.text or len(message.text < 1) or not f else message.text, 
            attachment=f)
        os.remove(media)
    