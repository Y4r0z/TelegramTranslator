from app.bot.vkBot import VkBot
from app.bot.tgBot import TgBot
import os
from app.commands import CommandHandler
from app.dataManager import DataManager
from  app.structs.message import Message
import logging as log
import asyncio
from asyncio import AbstractEventLoop

class Handler:

    def __init__(self, loop : AbstractEventLoop):
        self.loop = loop
        self.vk = VkBot(os.environ.get("VK_TOKEN"), loop)
        self.tg = TgBot(os.environ.get("TG_TOKEN"), loop)
        self.vk.newMessage.connect(self.vkMessage)
        self.tg.newMessage.connect(self.telegramMessage)
        
        self.data = DataManager()
        self.commands = CommandHandler(self.loop)


    def run(self):
        self.loop.create_task(self.vk.bot.run_polling())
        self.loop.create_task(self.tg.bot.run_polling())
        #self.loop.run_forever() Не требуется, т.к. телегам и так это делает

    def telegramMessage(self, message : Message):
        if not message.text or len(message.text) == 0: return
        #Так как список чатов нельзя получить, будем вручную сохранять все чаты, из которых нам написали
        if message.source not in self.data.tgChats:
            self.data.tgChats.append(message.source)
            self.data.save()
        log.info(message)
        self.translateTelegramMessage(message)

    def vkMessage(self, message : Message):
        log.info(message)
        if message.text[0] == '/':
            self.handleVkCommand(message)

    def handleVkCommand(self, message : Message):
        self.commands.run(message)

    def translateTelegramMessage(self, message : Message):
        for i in self.data.tgChats:
            if i != message.source: continue
            for j in i.subscribers:
                future = self.vk.sendMessage(j.id, message.text)
                self.loop.create_task(future)


    
    def exit(self):
        self.data.exit()

        
