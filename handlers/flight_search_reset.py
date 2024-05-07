# COMMAND HANDLER

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

# KEY BOARD IMPORTS
from utils.keyboards import single_button


async def flight_search_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.user_data.clear()
    menu = single_button(text='🔎 New Flight Search',
                         callback_data='start_flight_search')
    await context.bot.send_message(chat_id=chat_id, text='🤖 Alrighty, Your flight search has been reset.', reply_markup=menu, parse_mode=ParseMode.HTML)
