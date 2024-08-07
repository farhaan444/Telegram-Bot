# COMMAND HANDLER

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import os

# KEY BOARD IMPORTS
from utils.keyboards import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function is a COMMAND HANDLER. This function will only be called with the /start command"""
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    FILE_PATH = os.path.join('BotResponses', 'start_response.txt')
    
    with open(FILE_PATH, encoding='utf-8') as file:
        compitence = file.read()
    greeting = f'🤖 Hi {first_name} {last_name}! 👋 Welcome to Flight Spotter Bot. Here is what i can do:\n\n{compitence}\n\n Get Started! 👇'
    await context.bot.sendMessage(chat_id=update._effective_chat.id, text=greeting, reply_markup=main_menu, parse_mode=ParseMode.HTML)
