# -*- coding: utf-8 -*-
from bot.tg_bot import TelegramBot
from bot.vk_bot import VkBot
from messages.message_handler import MessageHandler
from file_manager import FileManager
from data_manager import DataManager
import asyncio

class Application:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.handler = MessageHandler()
        #load api
        #init api
        #save api
        self.tg = TelegramBot(self.loop, self.handler)
        self.vk = VkBot(self.loop, self.handler)
        # Load chats
        if FileManager().chatExists():
            chats = FileManager().loadChats()
            for i in chats['vk']:
                vk_chat = self.vk.addChat(int(i['id']))
                subs = []
                for j in i['subscriptions']:
                    if vk_chat.isSubscribedTo(int(j['id'])):
                        continue
                    vk_chat.subscriptions.append(self.tg.addChat(j['id']))
            for i in chats['tg']:
                if DataManager().tg_findById(int(i['id'])):
                    continue
                self.tg.addChat(i['id'])
        ############
        print('Программа запущена')
        self.loop.create_task(self.vk.bot.run_polling())
    
    def run(self):
        self.loop.run_forever()
        print('Конец')
        FileManager().saveChats()

    