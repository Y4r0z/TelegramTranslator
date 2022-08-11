# -*- coding: utf-8 -*-
from data_manager import DataManager
from bot.vk_bot import VkBot
from bot.tg_bot import TelegramBot
from telethon import utils
from chat.vk_chat import VkChat
from chat.tg_chat import TelegramChat
from messages.message import Message
from messages.media import Media, MediaType
from file_manager import FileManager
import typing
import os
class MessageHandler:
    def __init__(self):
        self.bots = []
        self.data = DataManager()
        self.file = FileManager()
        self.history : typing.List[Message] = [Message('none','none','none')]
    
    def add(self, bot):
        if bot not in self.bots:
            self.bots.append(bot)
        if bot.Platform == TelegramBot.Platform:
            self.tg = bot
        elif bot.Platform == VkBot.Platform:
            self.vk = bot
    
    async def handleMessage(self, obj, bot):
        if bot.Platform == VkBot.Platform:
            await self._handleVkMessage(obj)
        elif bot.Platform == TelegramBot.Platform:
            await self._handleTgMessage(obj)
    

    async def _handleTgMessage(self, event):
        chat = await event.get_chat()
        chatId = chat.id
        if not self.data.tg_findById(chatId):
            return
        sender = await event.get_sender()

        media = None
        if event.file:
            media = await self.file.downloadTgMedia(event, self.tg.bot)
        message = Message(utils.get_display_name(chat), utils.get_display_name(sender), event.text, media)

        self.history.append(message)
        if len(self.history) > 100: self.history.pop(0)

        print('tg:', event.text, end='')

        for i in self.data.vkChats:
            if i.isSubscribedTo(chatId):
                await self.vk.sendMessage(message, i.id)
                print(' =>', end='')
        print('')
        if message.media:
            os.remove(message.media.path)

    async def _handleVkMessage(self, message):
        text = message.text.lower()
        print('vk:', message.text, end=' ')
        if 'добав' in text:
            await self._vk_add(message)
            print('=>')
            return
        if not self.data.vk_findById(message.peer_id):
            return
        if 'подпи' in text and text[-2:] != 'ки':
            await self._vk_sub(message)
            print('=>',end='')
        elif 'отпи' in text:
            await self._vk_unsub(message)
            print('=>',end='')
        elif 'спис' in text or ('подп' in text and text[-2:] == 'ки'):
            await self._vk_list(message)
            print('=>',end='')
        elif 'стоп' in text:
            await self._vk_stop()
        print('')
    

    async  def _vk_add(self, message):
        peer = message.peer_id
        if not self.data.vk_findById(peer):
            chat = await VkChat.FromId(self.vk.bot.api, peer)
            self.data.vkChats.append(chat)
            await message.reply(f"Ваш локальный ID - {peer}, вы были подписаны на бота.")
        else:
            await message.reply(f"Вы уже подписаны на бота!")

    async def _vk_sub(self, message):
        text = message.text
        splitted = text.split(' ')
        if len(splitted) < 2:
            await message.reply(f"Для подписки на канал, напишите его название. Если он есть в подписках бота, он будет добавлен.")
            return
        chat : VkChat = self.data.vk_getById(message.peer_id)
        chatName : str = ' '.join(splitted[1:])
        tgChat = None
        try:
            tgChat = await TelegramChat.FromAny(self.tg.bot, chatName)
            if chat.isSubscribedTo(tgChat.id):
                raise Exception('Этот канал уже добавлен в ваши подписки!')
        except Exception as e:
            print("Не получилось добавить канал в подписки:\n", e)
            await message.reply(str(e))
            return
        chat.subscriptions.append(tgChat)
        self.data.tgChats.append(tgChat)
        await message.reply('Подписка на канал оформлена. Теперь сообщения из него будут перенаправлятся сюда.')
    
    async def _vk_unsub(self, message):
        text = message.text
        splitted = text.split(' ')
        if len(splitted) < 2:
            await message.reply(f"Для отписки от канала, напишите его название.")
            return
        chat : VkChat = self.data.vk_getById(message.peer_id)
        chatName : str = ' '.join(splitted[1:])
        for i in chat.subscriptions:
            if i.name.lower() != chatName.lower():
                continue
            tg_chat = i
            chat.subscriptions.remove(tg_chat)
            await message.reply(f'Канал {tg_chat.name} удален из подписок.')
            for j in self.data.vkChats:
                for k in j.subscriptions:
                    if k == tg_chat:
                        return
            self.data.tgChats.remove(tg_chat)
            return
        await message.reply("Канал не найден.")


        

    async def _vk_list(self, message):
        output = ['Список подписок:']
        chat = self.data.vk_getById(message.peer_id)
        output.extend([i.name for i in chat.subscriptions])
        await message.reply('\n'.join(output))

    async def _vk_stop(self):
        self.tg.bot.loop.stop()

    async def addSubcription(self, vkChat : VkChat, tgChatName : str):
        try:
            tgChat : TelegramChat = await TelegramChat.FromName(self.tg.bot, tgChatName)
        except Exception as e:
            raise e
            print(f"Can't add subscription {tgChatName} to {vkChat.name}.\n", e)
            return False
        if not self.data.tg_findById(tgChat.id):
            vkChat.subscriptions.append(tgChat)
            self.data.tgChats.append(tgChat)
        else:
           tgChat = self.data.tg_getById(tgChat.id)
           vkChat.subscriptions.append(tgChat)
        return True
    
    def parseMessage(self, message : Message):
        output = []
        last = self.history[-2]
        diff = Message.TimeDiff(message, last)
        if message.channel != last.channel or diff > 300:
            output.append(f'Новое сообщение из Telegram! Источник: {message.channel}.\n')
        if (message.author != last.author and message.author != message.channel) or diff > 60:
            output.append(f'{message.author}: ')
        output.append(message.text)
        return ''.join(output)
    
    async def stop(self):
        print('Принудительная остановка')


        