from app.structs.message import Message

from app.dataManager import DataManager

from typing import Callable

from asyncio import AbstractEventLoop
import logging as log


def cmpCommand(args, commands):
    for i in commands:
        if i in args:

            return True

    return False


class Command:

    def __init__(self, cmd : list[str], func : Callable, loop : AbstractEventLoop, description : str = None):

        self.keys = cmd

        self.function = func

        self.loop = loop

        self.description = description


    def execute(self, message : Message) -> None:

        args = message.text.split(' ')[1:]

        if cmpCommand(args, ['-h', '-help']):

            coro = message.message.reply(self.description)

            self.loop.create_task(coro)

        elif cmpCommand(args, ['-v', '-variant', '-variants']):

            coro = message.message.reply('Варианты команды:\n' + ' '.join(self.keys))

            self.loop.create_task(coro)
        else:

            self.function(message, self.loop)


    def check(self, message : Message) -> bool: 

        cmd = message.text.split(' ')[0].lower()

        return cmd in self.keys
    

    def run(self, message : Message) -> bool:

        if self.check(message):

            self.execute(message)

            return True

        return False





class CommandHandler:

    def __init__(self, loop : AbstractEventLoop):

        self.loop = loop

        self.commands : list[Command] = []

        self.initCommands()


    def run(self, message : Message):
        for i in self.commands:

            if i.run(message):

                return
            


    def addCommand(self, cmd : list[str], func, desc):

        self.commands.append(Command(cmd, func, self.loop, desc))


    def __getitem__(self, key):
        for i in self.commands:

            for j in i.keys:

                if j == key:

                    return i
    

    def initCommands(self):

        self.addCommand(['/список', '/каналы', '/чаты', '/все', '/list', '/all', '/группы'],

            sendChats, "Выводит список доступных для прослушивания каналов. Чтобы канал был доступен в этом списке, "

            + "в нем должно быть написано хотя бы одно сообщение при работе бота, чтобы он мог его обнаружить.")

        self.addCommand(['/подписка', '/подпиши', '/подписаться', '/sub', '/subscribe', '/добавить', '/add', '/добавь'],

            subscribeChat, 'Подписывает на определенный канал. Если вы подписаны на канал, то все сообщения из него будут приходить и сюда.'

            + '\nПример:\n/подписка Название канала\n/подписка ID_канала\n/подписка Название#ID')

        self.addCommand(['/отписка', '/отпиши', '/отписаться', '/unsub', '/unsubscribe', '/удалить', '/rem', '/удали', '/del', '/delete', '/remove'],

            unsubscribeChat, 'Отписывает от канала или чата. Сообщения из него больше не будут пересылаться сюда. Вызов команды такой же, как и у /подписка')

        self.addCommand(['/subs', '/подписки', '/cur', '/мои', '/my', '/текущие'], 

            sendSubsList, 'Выводит список каналов, на которые вы подписаны.')

        self.addCommand(['/команды', '/помощь', '/help', '/хелп', '/помоги', '/помогите'],

            sendHelp, 'Выводит список доступных команд.')












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

    text = 'Список доступных команд:\n/список\n/подписка\n/отписка\n/подписки\n/помощь'\
        + '\n\nСписок аргументов:\n -v -variant : варианты команды.\n-h -help : описание команды.'

    coro = message.message.reply(text)

    loop.create_task(coro)