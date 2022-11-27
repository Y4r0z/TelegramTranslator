from app.bot.vkBot import VkBot

from app.bot.tgBot import TgBot
import os

from  app.structs.message import Message
import logging as log


class Handler:

    def __init__(self, loop):

        self.loop = loop

        self.vk = VkBot(os.environ.get("VK_TOKEN"), loop)

        self.tg = TgBot(os.environ.get("TG_TOKEN"), loop)


        self.vk.newMessage.connect(self.m)

        self.tg.newMessage.connect(self.telegramMessage)


        self.chats = []



    def telegramMessage(self, message : Message):

        #Так как список чатов нельзя получить, будем вручную сохранять все чаты, из которых нам написали

        if message.source not in self.chats:

            self.chats.append(message.source)
        log.info(message)


    def m(self, mm):
        print(mm)



    def run(self):

        self.loop.create_task(self.vk.bot.run_polling())

        self.loop.create_task(self.tg.bot.run_polling())

        #self.loop.run_forever() Не требуется, телегам и так это делает