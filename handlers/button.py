# CALLBACKQUERY HANDLER
# THIS TEMPLATE DEFINES AND HANDLES THE CALLBACK QUERIES FROM ANY INLINE KEYBOARD

from telegram import Update
from telegram.ext import ContextTypes
from utils.flight_search import next_step
from utils.decorators import check_save_alert_limit
from utils.database import DB
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json

# HANDLER IMPORTS
from handlers.flight_alerts import flight_alerts
from handlers.help import help

# KEY BOARD IMPORTS
from utils.keyboards import flight_type_menu, main_menu, flight_result_menu, delete_all_menu, verify_del_menu


@check_save_alert_limit
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function is a CALLBACKQUERY HANDLER. This function will handler any callback queries from any inline keyboard"""
    callback = update.callback_query
    await callback.answer()
    chat_id = update.effective_chat.id
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    username = update.effective_chat.username
    db = DB()

    match callback.data:
        case 'start_flight_search':
            # Start flight search
            context.user_data.clear()
            context.chat_data.clear() #Clear chat data so that admin handler and conversation handler is not confused.
            context.user_data['Departure Airport'] = None
            context.user_data['Destination Airport'] = None
            context.user_data['Departure Date (Earliest)'] = None
            context.user_data['Departure Date (Latest)'] = None
            context.user_data['Minimum Lenth Of Stay'] = None
            context.user_data['Maximum Lenth Of Stay'] = None
            context.user_data['How Many Adults'] = None
            context.user_data['currency'] = 'ZAR'
            context.user_data['flight_type'] = None
            await context.bot.send_message(chat_id=chat_id, reply_markup=flight_type_menu, text='🤖 Please select option 👇')
        case 'oneway' | 'return' | 'multi-city':
            # sends option on flight search type
            # This will delete the inline keyboard after user has clicked on option
            current_menu = callback
            await current_menu.delete_message()

            if callback.data == 'oneway':
                context.user_data['flight_type'] = 'ONEWAY'
                context.user_data['Minimum Lenth Of Stay'] = 'VOID'
                context.user_data['Maximum Lenth Of Stay'] = 'VOID'
                await next_step(update=update, context=context)
            elif callback.data == 'return':
                context.user_data['flight_type'] = 'RETURN'
                await next_step(update=update, context=context)
            elif callback.data == 'multi-city':
                context.user_data.clear()
                context.user_data['Departure Airport'] = None
                context.user_data['Destination Airport'] = None
                context.user_data['date_from'] = None
                context.user_data['How Many Adults'] = None
                context.user_data['currency'] = 'ZAR'
                context.user_data['flight_type'] = 'MULTI-CITY'
                context.user_data['requests'] = []
                await next_step(update=update, context=context)
        case 'main_menu':
            # This will send the user the main menu with all available options.
            await context.bot.send_message(chat_id=chat_id, text='🤖 What can i do for you? 👇', reply_markup=main_menu)
        case 'track_flight':
            # This will add flight data to db to be tracked.
            if 'link' in context.user_data:
                if context.user_data["flight_type"] == "ONEWAY" or context.user_data["flight_type"] == "RETURN":

                    menu = flight_result_menu(
                        link=context.user_data['link'], tracked=True)

                    Departure_Airport = context.user_data['Departure Airport']
                    Destination_Airport = context.user_data['Destination Airport']
                    Departure_Date_Earliest = context.user_data['Departure Date (Earliest)']
                    Departure_Date_Latest = context.user_data['Departure Date (Latest)']
                    Minimum_Lenth_Of_Stay = context.user_data['Minimum Lenth Of Stay']
                    Maximum_Lenth_Of_Stay = context.user_data['Maximum Lenth Of Stay']
                    How_Many_Adults = context.user_data['How Many Adults']
                    currency = context.user_data['currency']
                    flight_type = context.user_data['flight_type']
                    price = context.user_data['price']

                    # add user if not exist
                    user = db.cursor.execute(
                        "SELECT * FROM users WHERE chat_id = ?", (chat_id,)).fetchone()
                    if user != None:
                        db.add_flight_data(chat_id=chat_id, fly_from=Departure_Airport, fly_to=Destination_Airport, date_from=Departure_Date_Earliest, date_to=Departure_Date_Latest,
                                           nights_from=Minimum_Lenth_Of_Stay, nights_to=Maximum_Lenth_Of_Stay, adults=How_Many_Adults, curr=currency, flight_type=flight_type, current_price=price)
                        db.close()
                        await callback.edit_message_reply_markup(reply_markup=menu)
                    else:
                        db.add_user(chat_id=chat_id, username=username,
                                    first_name=first_name, last_name=last_name)
                        db.add_flight_data(chat_id=chat_id, fly_from=Departure_Airport, fly_to=Destination_Airport, date_from=Departure_Date_Earliest, date_to=Departure_Date_Latest,
                                           nights_from=Minimum_Lenth_Of_Stay, nights_to=Maximum_Lenth_Of_Stay, adults=How_Many_Adults, curr=currency, flight_type=flight_type, current_price=price)
                        db.close()
                        await callback.edit_message_reply_markup(reply_markup=menu)
                elif context.user_data["flight_type"] == "MULTI-CITY":

                    menu = flight_result_menu(
                        link=context.user_data['link'], tracked=True)

                    Departure_Airport = "VOID"
                    Destination_Airport = "VOID"
                    Departure_Date_Earliest = "VOID"
                    Departure_Date_Latest = "VOID"
                    Minimum_Lenth_Of_Stay = "VOID"
                    Maximum_Lenth_Of_Stay = "VOID"
                    How_Many_Adults = context.user_data['How Many Adults']
                    currency = context.user_data['currency']
                    flight_type = context.user_data['flight_type']
                    price = context.user_data['price']
                    # Convert List to string to store to DB
                    multi_city_req = json.dumps(context.user_data['requests'])

                    # add user if not exist
                    user = db.cursor.execute(
                        "SELECT * FROM users WHERE chat_id = ?", (chat_id,)).fetchone()

                    if user != None:
                        db.add_flight_data(chat_id=chat_id, fly_from=Departure_Airport, fly_to=Destination_Airport, date_from=Departure_Date_Earliest, date_to=Departure_Date_Latest,
                                           nights_from=Minimum_Lenth_Of_Stay, nights_to=Maximum_Lenth_Of_Stay, adults=How_Many_Adults, curr=currency, flight_type=flight_type, current_price=price, multi_city_req=multi_city_req)
                        db.close()
                        await callback.edit_message_reply_markup(reply_markup=menu)
                    else:
                        db.add_user(chat_id=chat_id, username=username,
                                    first_name=first_name, last_name=last_name)
                        db.add_flight_data(chat_id=chat_id, fly_from=Departure_Airport, fly_to=Destination_Airport, date_from=Departure_Date_Earliest, date_to=Departure_Date_Latest,
                                           nights_from=Minimum_Lenth_Of_Stay, nights_to=Maximum_Lenth_Of_Stay, adults=How_Many_Adults, curr=currency, flight_type=flight_type, current_price=price, multi_city_req=multi_city_req)
                        db.close()
                        await callback.edit_message_reply_markup(reply_markup=menu)

            else:
                menu = flight_result_menu(link=None, err=True)
                await callback.edit_message_reply_markup(reply_markup=menu)
        case 'get_flight_alerts':
            # This gets list of all saved flight data that is been tracked and sends to user
            await flight_alerts(update, context)
        case 'verify_del' | 'no_del':
            # This sends a user a confirmation to delete all flight data. 
            if callback.data == 'verify_del':
                await context.bot.send_message(chat_id=chat_id, text='🤖 Are you sure you want delete all your flight data?', reply_markup=verify_del_menu)
            elif callback.data == 'no_del':
                current_menu = callback
                await current_menu.delete_message()
        case 'del_all_FA':
            # This deletes all tracked flight data from db
            db.del_all_flight_data(chat_id=chat_id)
            db.close()
            menu = delete_all_menu(success=True)
            await callback.edit_message_text(text='You have no flight alerts yet. Start a flight search and create a new flight alert.', reply_markup=menu)
        case 'add_flight':
            # This will add flights to the flight list in the multi-city search
            try:
                if len(context.user_data['requests']) < 8:
                    context.user_data['Departure Airport'] = None
                    context.user_data['Destination Airport'] = None
                    context.user_data['date_from'] = None
                    await next_step(update=update, context=context)
                else:
                    menu = [[InlineKeyboardButton(
                        '🔎 Get result', callback_data='multicity_result')]]
                    menu = InlineKeyboardMarkup(menu)
                    await context.bot.send_message(chat_id=chat_id, text='❗You cannot add anymore flights.', reply_markup=menu)
            except KeyError:
                # Exception is raised if flight search was reset
                await context.bot.send_message(chat_id=chat_id, text="🤖 Your flight search has been reset. Please select option 👇", reply_markup=flight_type_menu)
        case 'multicity_result':
            # This will call function to get and send out multi-city result
            try:
                _ = context.user_data['flight_type']
                await next_step(update=update, context=context, MT_result=True)
            except KeyError:
                # Exception is thrown if flight search was reset
                await context.bot.send_message(chat_id=chat_id, text="🤖 Your flight search has been reset. Please select option 👇", reply_markup=flight_type_menu)
        case 'help':
            # This will call the help command handler
            await help(update=update, context=context)
        case 'admin-FTjob-set':
            # This activates admin message handler and sends response for admin to set flight tracker job.
            # user_data will be reset to avoid bot confusion when handling data in message handler.
            context.user_data.clear()
            context.chat_data['set'] = 'Set Flight Tracker Job'
            reply = "🤖 Enter a number in seconds to set the Job run interval. e.g 900. Please note you cannot enter a value less than 900 seconds."
            context.chat_data['status'] = "verified"
            await context.bot.send_message(chat_id=chat_id, text=reply)
        case 'admin-FTlimit-set':
            # This activates admin message handler and sends response for admin to set flight alert limit.
            # user_data will be reset to avoid bot confusion when handling data in message handler.
            context.user_data.clear()
            context.chat_data['set'] = 'Set Flight Alert Limit' 
            reply = "🤖 Enter a number to set the flight alert limit. Set to 0 for unlimited flight alerts."
            context.chat_data['status'] = "verified"
            await context.bot.send_message(chat_id=chat_id, text=reply)