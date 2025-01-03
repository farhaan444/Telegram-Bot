# COMMAND HANDLER

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import os

# KEY BOARD IMPORTS
from utils.keyboards import main_menu_redirect


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function is a Telegram Bot Command Handler.
    It is invoked when the user types /help in a Telegram chat.
    The function will return a message with the help text.
    The message will also include a button to go back to the main menu.
    """
    
    FILE_PATH = os.path.join('BotResponses', 'help.txt')

    with open(FILE_PATH, encoding='utf-8') as file:
        help_file = file.read()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_file, parse_mode=ParseMode.HTML, reply_markup=main_menu_redirect)
