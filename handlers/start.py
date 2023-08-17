# COMMAND HANDLER

from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function is a COMMAND HANDLER. This function will only be called with the /start command"""
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    compitence = '▪️ Search for cheap flights 🔎\n▪️ Track flight prices 👀\n▪️ Notify you if flight prices drop 🔔'
    greeting = f'Hi {first_name} {last_name}!👋 Welcome to Deal Spotter ZA. Here is what i can do:\n\n{compitence}\n\n Get Started! 👇'
    await context.bot.sendMessage(chat_id=update._effective_chat.id, text=greeting, reply_markup=main_menu)
