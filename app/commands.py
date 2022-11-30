from app.structs.message import Message
from app.dataManager import DataManager
from typing import Callable
from asyncio import AbstractEventLoop
import logging as log

class Command:
    def __init__(self, cmd : list[str], func : Callable, loop : AbstractEventLoop):
        self.keys = cmd
        self.function = func
        self.loop = loop

    def execute(self, message : Message) -> None:
        self.function(message, self.loop)

    def check(self, message : Message) -> bool: 
        cmd = message.text.split(' ')[0].lower()
        return cmd in self.keys
    
    def run(self, message : Message) -> bool:
        if self.check(message):
            self.execute(message)
            return True
        return False


class Commands:
    СhatsList = ['/список', '/каналы', '/чаты', '/все', '/list', '/all', '/группы']
    SubsList = ['/subs', '/подписки', '/cur', '/мои', '/my', '/текущие']
    Susbcribe = ['/подписка', '/подпиши', '/подписаться', '/sub', '/subscribe', '/добавить', '/add', '/добавь']
    Help = ['/help', '/помощь', '/помоги', '/хелп', '/команды']

class CommandHandler:
    def __init__(self, loop : AbstractEventLoop):
        self.loop = loop
        self.commands : list[Command] = []
        self.initCommands()

    def run(self, message : Message):
        for i in self.commands:
            if i.run(message):
                return
            

    def addComand(self, cmd : list[str], func):
        self.commands.append(Command(cmd, func, self.loop))

    def __getitem__(self, key):
        for i in self.commands:
            for j in i.keys:
                if j == key:
                    return i
    
    def initCommands(self):
        self.addComand(['/список', '/каналы', '/чаты', '/все', '/list', '/all', '/группы'],
            sendChats)
        self.addComand(['/подписка', '/подпиши', '/подписаться', '/sub', '/subscribe', '/добавить', '/add', '/добавь'],
            subscribeChat)
        self.addComand(['/отдписка', '/отпиши', '/отписаться', '/unsub', '/unsubscribe', '/удалить', '/rem', '/удали', '/del', '/delete', '/remove'],
            unsubscribeChat)
        self.addComand(['/subs', '/подписки', '/cur', '/мои', '/my', '/текущие'], 
            sendSubsList)











def sendChats(message : Message, loop : AbstractEventLoop):
    log.info("Отправка списка чатов")
    text = "Список доступных для прослушивания источников:\n" + '\n'.join([str(i) for i in DataManager().tgChats])
    coro = message.message.reply(text)
    loop.create_task(coro)

def subscribeChat(message : Message, loop : AbstractEventLoop):
        arg = ' '.join(message.text.split(' ')[1:])
        text = ''
        if DataManager().subscribe(arg, message.source):
            text = 'Подписка совершена.'
            DataManager().save()
        else:
            text = "Такой канал не найден. Проверьте название, id канала или попробуйте отправить сообщение в нужный вам канал, чтобы бот увидел его."
        coro = message.message.reply(text)
        loop.create_task(coro)
    
def sendSubsList(message: Message, loop : AbstractEventLoop):
        source = message.source.id
        res = []
        for i in DataManager().tgChats:
            for j in i.subscribers:
                if j.id != source:
                    continue
                res.append(i.name)
        text = "Ваши подписки:\n" + '\n'.join(res)
        coro = message.message.reply(text)
        loop.create_task(coro)

def unsubscribeChat(message : Message, loop : AbstractEventLoop):
    arg = ' '.join(message.text.split(' ')[1:])
    if DataManager().unsubscribe(arg, message.source):
        text = 'Вы успешно отписались.'
        DataManager().save()
    else:
        text = "Такой канал не найден."
    coro = message.message.reply(text)
    loop.create_task(coro)

def sendHelp(message: Message, loop : AbstractEventLoop):
    pass
