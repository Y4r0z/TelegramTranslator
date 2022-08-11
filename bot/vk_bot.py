# -*- coding: utf-8 -*-
from vkbottle.bot import Bot, Message, Blueprint
from vkbottle.tools import DocMessagesUploader, PhotoMessageUploader, AudioUploader, VideoUploader, VoiceMessageUploader
from api_data import vk_token, tg_api_id, tg_api_hash
from chat.vk_chat import VkChat
from messages.message import Message
from messages.media import Media, MediaType
from data_manager import DataManager
from bot.bot import ChatBot
import platforms
import os

class VkBot(ChatBot):
    Platform = platforms.Platform.vkontakte
    def __init__(self, loop, handler):
        super().__init__(handler, Bot(vk_token, loop = loop))
        self._initHandlers()
        print('Бот ВК загружен!')
    
    def _initHandlers(self):
        @self.bot.on.message()
        async def defaultHandler(message : Message):
            if len(message.text) == 0: return
            if message.text[0] != '!': return
            await self.handler.handleMessage(message, self)
            

    async def sendMessage(self, message : Message, destination):
        output = self.parseMessage(message)
        if message.media:
            if message.media.type == MediaType.photo:
                media = await PhotoMessageUploader(self.bot.api).upload(
                    message.media.path, peer_id = destination)
            elif message.media.type == MediaType.audio:
                media = await VoiceMessageUploader(self.bot.api).upload(
                    message.media.name, message.media.path, peer_id = destination)
            else:
                media = await DocMessagesUploader(self.bot.api).upload(
                    message.media.name, message.media.path, peer_id = destination)
            await self.bot.api.messages.send(peer_id=destination, message=output, random_id = 0, attachment = media)
        else:
            if len(output) > 0:
                await self.bot.api.messages.send(peer_id=destination, message=output, random_id = 0)
    

    def parseMessage(self, message : Message):
        output = []
        last = self.handler.history[-2]
        diff = Message.TimeDiff(message, last)
        if message.channel != last.channel or diff > 120:
            output.append(f'Новое сообщение из Telegram! Источник: {message.channel}.\n')
        if (message.author != last.author and message.author != message.channel) or diff > 30:
            output.append(f'{message.author}: ')
        output.append(message.text)
        return ''.join(output)
    

    def addChat(self, chat_id) -> VkChat:
        if DataManager().vk_findById(chat_id):
            return DataManager().vk_getById(chat_id)
        task = VkChat.FromId(self.bot.api, chat_id)
        chat = self.bot.loop.run_until_complete(task)
        DataManager().vkChats.append(chat)
        print(f'Чат {chat.name} добавлен в VK.')
        return chat
    