# -*- coding: utf-8 -*-
from bot.tg_bot import TelegramBot
from bot.vk_bot import VkBot
from messages.message_handler import MessageHandler
import asyncio

class Application:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        handler = MessageHandler()
        self.tg = TelegramBot(self.loop, handler)
        self.vk = VkBot(self.loop, handler)
        print('Программа запущена')
        self.loop.create_task(self.vk.bot.run_polling())
    
    def run(self):
        self.loop.run_forever()
        print('Конец')

    