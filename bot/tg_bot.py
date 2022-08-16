# -*- coding: utf-8 -*-
from telethon import TelegramClient, events, utils
from data_manager import DataManager
from file_manager import FileManager
from chat.tg_chat import TelegramChat
from bot.bot import ChatBot
import platforms
import os
class TelegramBot(ChatBot):
    Platform = platforms.Platform.telegram
    def __init__(self, loop, handler):
        if len(handler.bots) != 0:
            raise "Необходимо инициализировать бот Телеграма первым!"
            return
        if not os.path.exists('sessions/'):
            os.makedirs('sessions/')
        api = FileManager().loadApi()
        super().__init__(handler, TelegramClient('sessions/session', api['tg_id'], api['tg_hash'], loop = loop))
        self.bot.start()
        self._initHandlers()
        print('Бот Телеграм загружен!')

    def _initHandlers(self):
        @self.bot.on(events.NewMessage)
        async def defaultHandler(event):
            await self.handler.handleMessage(event, self)
    
    def addChat(self, chat_id) -> TelegramChat:
        if DataManager().tg_findById(chat_id):
            return DataManager().tg_getById(chat_id)
        task = TelegramChat.FromId(self.bot, chat_id)
        chat = self.bot.loop.run_until_complete(task)
        DataManager().tgChats.append(chat)
        print(f'Чат {chat.name} добавлен в Tg.')
        return chat

        
    







