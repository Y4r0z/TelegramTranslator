import os
import logging as log

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatMember, constants
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler

from app.bot.bot import ChatBot


class TgBot(ChatBot):
    def __init__(self, api, loop):
        super().__init__()
        self.loop = loop

        self.bot = ApplicationBuilder().token(os.getenv("TG_TOKEN")).build()

        self.bot.add_handler(MessageHandler(filters.COMMAND, self.handleCommand))
        self.bot.add_handler(MessageHandler(filters.TEXT, self.handleMessage))

        self.loop.create_task(self.bot.run_polling())


    async def handleCommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chatId = int(update.effective_chat.id)
        userId = int(update.effective_user.id)
        text = update.message.text
        log.info(f"\nNew command from user {update.effective_user.name} #{userId}: {text}")
        self.newCommand.emit(text)
       
    
    async def handleMessage(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chatId = int(update.effective_chat.id)
        userId = int(update.effective_user.id)
        text = update.message.text
        log.info(f"\nNew message from user {update.effective_user.name} #{userId}: {text}")
        self.newMessage.emit(text)

