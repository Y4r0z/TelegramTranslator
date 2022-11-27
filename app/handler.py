from app.bot.vkBot import VkBot
from app.bot.tgBot import TgBot
import os

class Handler:
    def __init__(self, loop):
        vk = VkBot(os.environ.get("VK_TOKEN"), loop)
        tg = TgBot(os.environ.get("TG_TOKEN"), loop)
        vk.newMessage.connect(self.m)
        vk.newCommand.connect(self.c)
        tg.newMessage.connect(self.m)
        tg.newCommand.connect(self.c)


    def c(self, cc):
        print(f"cc: {cc} \n\n\n\n\n\n")
    def m(self, mm):
        print(f"mm: {mm} \n\n\n\n\n\n")