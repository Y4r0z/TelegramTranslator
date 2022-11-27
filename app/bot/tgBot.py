import os
import logging as log

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatMember, constants
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler


from app.bot.bot import ChatBot

from app.structs.message import Message
from app.structs.object.channel import Channel
from app.structs.object.user import User

class TgBot(ChatBot):
    def __init__(self, api, loop):
        super().__init__()
        self.loop = loop

        self.bot = ApplicationBuilder().token(os.getenv("TG_TOKEN")).build()

        self.bot.add_handler(MessageHandler(~filters.COMMAND, self.handleMessage))
        self.bot.add_handler(MessageHandler(filters.COMMAND, self.handleMessage))
       
    
    async def handleMessage(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.type == constants.ChatType.PRIVATE:
            return
        chat = Channel(update.effective_chat.title, int(update.effective_chat.id))
        if update.effective_user is None:
            user = chat
        else:
            user = User(update.effective_user.full_name, int(update.effective_user.id))
        text = update.effective_message.text
        self.newMessage.emit(Message(chat, user, text, _id = update.effective_message.id))

