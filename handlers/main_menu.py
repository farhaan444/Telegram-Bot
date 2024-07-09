# COMMAND HANDLER

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from random import randint
import os

# KEY BOARD IMPORTS
from utils.keyboards import main_menu


async def handler_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    FILE_PATH = os.path.join('BotResponses', 'main_menu.txt')

    with open(FILE_PATH, encoding='utf-8') as file:
        replies = file.readlines()
    reply = replies[randint(0, (len(replies) - 1))]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🤖 {reply}", reply_markup=main_menu, parse_mode=ParseMode.HTML)
