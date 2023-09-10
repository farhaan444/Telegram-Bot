# MESSAGE HANDLER

# PTB IMPORTS
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def unknown_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='🤖 Sorry, i do not understand this commmand.', parse_mode=ParseMode.HTML)
