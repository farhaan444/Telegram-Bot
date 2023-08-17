# MESSAGE HANDLER

from telegram import Update
from telegram.ext import ContextTypes
from utils.flight_search import get_airports, format_date, is_date_in_past, validate_number, next_step

# KEY BOARD IMPORTS
from utils.keyboards import airport_menu


async def converstaion(update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs):
    """This function is a MESSAGE HANDLER. This function will optionaly take a keyword argument to initate a chat from the bot"""

    chat_id = update.effective_chat.id
    text = update.message.text.strip()

    # ------------------------------ FLIGHTS SEARCH ---------------------------------------#

    for key, value in context.user_data.items():
        if value == None:
            if key == 'Departure Airport':
                if ':' not in text:
                    airports_list = get_airports(location=text)
                    if airports_list == 'Connection Error':
                        await context.bot.send_message(chat_id=chat_id, text='🤖 Today is not my day! I am having connection issues, please try again later.')
                        break
                    elif airports_list == None:
                        await context.bot.send_message(chat_id=chat_id, text='😕 I cannot find any airport with that city you provided. Please, try again.')
                        break
                    else:
                        airports_list = airport_menu(airports=airports_list)
                        await context.bot.send_message(chat_id=chat_id, reply_markup=airports_list, text='Please choose a Airport from the list 👇')
                        break
                else:
                    colon_index = text.find(':')
                    iata = text[colon_index + 1:]
                    context.user_data[key] = iata.lstrip()
                    await next_step(update=update, context=context)
                    break

            if key == 'Destination Airport':
                if ':' not in text:
                    airports_list = get_airports(location=text)
                    if airports_list == 'Connection Error':
                        await context.bot.send_message(chat_id=chat_id, text='🤖 Today is not my day! I am having connection issues, please try again later.')
                        break
                    elif airports_list == None:
                        await context.bot.send_message(chat_id=chat_id, text='😕 I cannot find any airport with that city you provided. Please, try again.')
                        break
                    else:
                        airports_list = airport_menu(airports=airports_list)
                        await context.bot.send_message(chat_id=chat_id, reply_markup=airports_list, text='Please choose a Airport from the list 👇')
                        break
                else:
                    colon_index = text.find(':')
                    iata = text[colon_index + 1:]
                    context.user_data[key] = iata.lstrip()
                    await next_step(update=update, context=context)
                    break

            if key == 'Departure Date (Earliest)' or key == 'Departure Date (Latest)':
                validate_date_format = format_date(date=text)
                if validate_date_format == None:
                    error_msg = '😕 Ooops! Your date format is wrong. Please enter date again in this format Day/Month/Year e.g 01/01/2023'
                    await context.bot.send_message(chat_id=chat_id, text=error_msg)
                    break
                elif is_date_in_past(text) is False:
                    error_msg = '🤨 You Honestly expect me to search with date that is in the past tense? Please enter a present or future date'
                    await context.bot.send_message(chat_id=chat_id, text=error_msg)
                    break
                else:
                    context.user_data[key] = text
                    await next_step(update=update, context=context)
                    break

            if key == 'Minimum Lenth Of Stay' or key == 'Maximum Lenth Of Stay' or key == 'How Many Adults':
                validate_num = validate_number(number=text)
                if validate_num is False:
                    error_msg = '🫤 Seriously, its not hard. Try again and enter only a number, e.g 2'
                    await context.bot.send_message(chat_id=chat_id, text=error_msg)
                    break
                else:
                    if key == 'How Many Adults':
                        context.user_data[key] = int(text)
                        await next_step(update=update, context=context)
                        break
                    else:
                        context.user_data[key] = text
                        await next_step(update=update, context=context)
                        break
