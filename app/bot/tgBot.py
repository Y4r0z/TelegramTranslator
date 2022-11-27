import os
import logging as log

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatMember, constants
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler

from app.bot.bot import ChatBot

from app.stucts.message import Message
from app.stucts.channel import Channel
from app.stucts.user import User

class TgBot(ChatBot):
    def __init__(self, api, loop):
        super().__init__()
        self.loop = loop

        self.bot = ApplicationBuilder().token(os.getenv("TG_TOKEN")).build()

        self.bot.add_handler(MessageHandler(filters.COMMAND, self.handleCommand))
        self.bot.add_handler(MessageHandler(filters.TEXT, self.handleMessage))

    async def handleCommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = Channel(update.effective_chat.full_name, int(update.effective_chat.id))
        if update.effective_user is None:
            user = chat
        else:
            user = User(update.effective_user.full_name, int(update.effective_user.id))
        text = update.effective_message.text
        self.newCommand.emit(Message(chat, user, text))
       
    
    async def handleMessage(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = Channel(update.effective_chat.title, int(update.effective_chat.id))
        if update.effective_user is None:
            user = chat
        else:
            user = User(update.effective_user.full_name, int(update.effective_user.id))
        text = update.effective_message.text
        self.newMessage.emit(Message(chat, user, text))

