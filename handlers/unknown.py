# MESSAGE HANDLER

# PTB IMPORTS
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

# KEY BOARD IMPORTS
from utils.keyboards import main_menu_redirect


async def unknown_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This is a Telegram Bot Message Handler.
    It is invoked when the user sends a command that the bot does not understand.
    The function will return a message with a sorry message and a button to go back to the main menu.
    """
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text='🤖 Sorry, i do not understand this command.', reply_markup=main_menu_redirect, parse_mode=ParseMode.HTML)
