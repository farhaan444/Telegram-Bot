# THIS TEMPLATE DEFINES AND HANDLES THE CALLBACK QUERIES FROM ANY INLINE KEYBOARD
# CALLBACKQUERY HANDLER

from telegram import Update
from telegram.ext import ContextTypes
from utils.flight_search import next_step

# KEY BOARD IMPORTS
from utils.keyboards import flight_type_menu, main_menu


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function is a CALLBACKQUERY HANDLER. This function will handler any callback queries from any inline keyboard"""
    callback = update.callback_query
    await callback.answer()
    callback_data = callback.data
    chat_id = update.effective_chat.id

    if callback_data == 'start_flight_search':
        context.user_data.clear()
        context.user_data['Departure Airport'] = None
        context.user_data['Destination Airport'] = None
        context.user_data['Departure Date (Earliest)'] = None
        context.user_data['Departure Date (Latest)'] = None
        context.user_data['Minimum Lenth Of Stay'] = None
        context.user_data['Maximum Lenth Of Stay'] = None
        context.user_data['How Many Adults'] = None
        context.user_data['currency'] = 'ZAR'
        context.user_data['flight_type'] = None
        await context.bot.send_message(chat_id=chat_id, reply_markup=flight_type_menu, text='Please select option 👇')

    if callback_data == 'oneway' or callback_data == 'return':
        # This will delete the inline keyboard after user has clicked on option
        current_menu = callback
        await current_menu.delete_message()

        if callback_data == 'oneway':
            context.user_data['flight_type'] = 'ONEWAY'
            context.user_data['Minimum Lenth Of Stay'] = 'VOID'
            context.user_data['Maximum Lenth Of Stay'] = 'VOID'
            await next_step(update=update, context=context)

        elif callback_data == 'return':
            context.user_data['flight_type'] = 'RETURN'
            await next_step(update=update, context=context)

    if callback_data == 'main_menu':
        await context.bot.send_message(chat_id=chat_id, text='🤖 What can i do for you? 👇', reply_markup=main_menu)
