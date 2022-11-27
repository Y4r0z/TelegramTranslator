from app.bot.vkBot import VkBot
from app.bot.tgBot import TgBot
import os
from app.commands import Commands
from app.dataManager import DataManager
from  app.structs.message import Message
import logging as log
import asyncio

class Handler:

    def __init__(self, loop):
        self.loop = loop
        self.vk = VkBot(os.environ.get("VK_TOKEN"), loop)
        self.tg = TgBot(os.environ.get("TG_TOKEN"), loop)
        self.vk.newMessage.connect(self.vkMessage)
        self.tg.newMessage.connect(self.telegramMessage)
        
        self.data = DataManager()

    def run(self):
        self.loop.create_task(self.vk.bot.run_polling())
        self.loop.create_task(self.tg.bot.run_polling())
        #self.loop.run_forever() Не требуется, т.к. телегам и так это делает
    

    def telegramMessage(self, message : Message):
        #Так как список чатов нельзя получить, будем вручную сохранять все чаты, из которых нам написали
        if message.source not in self.data.tgChats:
            self.data.tgChats.append(message.source)
        log.info(message)
        self.translateTelegramMessage(message)


    def vkMessage(self, message : Message):
        log.info(message)
        if message.text[0] == '/':
            self.handleVkCommand(message)

    def handleVkCommand(self, message : Message):
        cmd = message.text.split(' ')[0]
        if cmd in Commands.СhatsList:
            self.sendChats(message)
        elif cmd in Commands.Susbcribe:
            self.subscribeChat(message)

    def translateTelegramMessage(self, message : Message):
        for i in self.data.tgChats:
            if i != message.source: continue
            for j in i.subscribers:
                future = self.vk.sendMessage(j.id, message.text)
                self.loop.create_task(future)




    def sendChats(self, message : Message):
        log.info("Отправка списка чатов")
        future = self.vk.sendMessage(message.source.id, "Список доступных для прослушивания источников:\n"
        + '\n'.join([str(i) for i in self.data.tgChats]))
        self.loop.create_task(future)
    
    def subscribeChat(self, message : Message):
        arg = ' '.join(message.text.split(' ')[1:])
        text = ''
        if self.data.subscribe(arg, message.source):
            text = 'Подписка совершена.'
        else:
            text = "Такой канал не найден. Проверьте название, id канала или попробуйте отправить сообщение в нужный вам канал, чтобы бот увидел его."
        future = self.vk.sendMessage(message.source.id, text)
        self.loop.create_task(future)

        
