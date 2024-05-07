import config
from datetime import datetime
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import ContextTypes
import aiohttp
import logging

# KEY BOARD IMPORTS
from utils.keyboards import adults_menu, flight_result_menu, main_menu_redirect, multicity_menu

logger = logging.getLogger(__name__)


async def get_airports(location):
    """This function calls the location kiwi api and returns airport name and iata code"""

    header = {'apikey': config.KIWI_API_KEY_STD}
    endpoint = 'https://api.tequila.kiwi.com/locations/query'
    params = {
        'term': location,
        'location_types': 'airport'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=endpoint, params=params, headers=header) as response:
                response.raise_for_status()
                data = await response.json()
    except Exception as error:
        logger.error(msg="Get Airports Error", exc_info=error)
        return 'Connection Error'
    else:
        results = data['results_retrieved']
        try:
            if results == 0:
                raise IndexError
            airports = []
            for i in range(results):
                airport = f'{data["locations"][i]["name"]}: {data["locations"][i]["code"]}'
                airports.append(airport)
        except IndexError:
            airports = None
            return airports
        else:
            return airports


def format_date(date):
    """This check if the user has inputed the date in the correct format. 
    If not this function will try and format the date.
    Date format Day/Month/Year. """

    if '/' in date:
        try:
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            formated_date = date_obj.strftime('%d/%m/%Y')
        except ValueError:
            return None
        else:
            return formated_date
    else:
        return None


def is_date_in_past(date):
    """This function will check date presence and return true if date is in the present or future and return false if it is in the past."""
    input_date = datetime.strptime(date, "%d/%m/%Y").date()
    today = datetime.today().date()
    if input_date > today:
        return True
    elif input_date == today:
        return True
    else:
        return False


def validate_number(number):
    """This function check if arg is a number and not a string number"""
    try:
        int(number)
        return True
    except ValueError:
        return False


def is_int_0(number):
    """This function check if the arg is == 0"""
    if int(number) == 0:
        return True
    else:
        return False


async def search_flights(user_data):
    """This function takes in a dict arg of all user data need to call api to search for flights.
    The function will also search and get the cheapest price. 
    Returns a list: price, destination and departure"""

    header = {'apikey': config.KIWI_API_KEY_STD}
    endpoint = 'https://api.tequila.kiwi.com/v2/search'
    if user_data['flight_type'] == 'ONEWAY':
        params = {
            'fly_from': user_data['Departure Airport'],
            'fly_to': user_data['Destination Airport'],
            'date_from': user_data['Departure Date (Earliest)'],
            'date_to': user_data['Departure Date (Latest)'],
            'adults': user_data['How Many Adults'],
            'curr': user_data['currency'],
            'limit': 1000,
        }
    elif user_data['flight_type'] == 'RETURN':
        params = {
            'fly_from': user_data['Departure Airport'],
            'fly_to': user_data['Destination Airport'],
            'date_from': user_data['Departure Date (Earliest)'],
            'date_to': user_data['Departure Date (Latest)'],
            'nights_in_dst_from': user_data['Minimum Lenth Of Stay'],
            'nights_in_dst_to': user_data['Maximum Lenth Of Stay'],
            'adults': user_data['How Many Adults'],
            'curr': user_data['currency'],
            'limit': 1000,
        }
    elif user_data['flight_type'] == 'MULTI-CITY':
        header = {'apikey': config.KIWI_API_KEY_MULTICITY}
        endpoint = 'https://api.tequila.kiwi.com/v2/flights_multi'
        params = {
            "requests": [{"fly_to": i['fly_to'], "fly_from": i["fly_from"], "date_to": i["date_from"], "date_from": i["date_from"], "adults": i['adults'], "curr": user_data['currency'], "limit": 1000} for i in user_data['requests']]
        }

    if user_data['flight_type'] == 'ONEWAY' or user_data['flight_type'] == 'RETURN':
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=endpoint, params=params, headers=header) as response:
                    response.raise_for_status()
                    data = await response.json()
        except Exception as error:
            logger.error(
                "Flight Search: Oneway & Return Execption", exc_info=error)
            return False
        else:
            price_list = []
            data_len = len(data['data'])
            try:
                for i in range(data_len):
                    price_list.append(data['data'][i]['price'])
                min_price = min(price_list)
                for i in range(data_len):
                    if data['data'][i]['price'] == min_price:
                        link = data['data'][i]['deep_link']
                        destination = data['data'][i]['cityTo']
                        departure = data['data'][i]['cityFrom']
                    result = [min_price, link,
                              destination, departure, data_len]
                    break
            except (IndexError, ValueError):
                return None
            else:
                return result
    elif user_data['flight_type'] == 'MULTI-CITY':
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=endpoint, json=params, headers=header) as response:
                    response.raise_for_status()
                    data = await response.json()
        except Exception as error:
            logger.error("Flight Search: Multi-City Exception", exc_info=error)
            return False
        else:
            price_list = []
            data_len = len(data)
            try:
                for i in range(data_len):
                    price_list.append(data[i]["price"])
                min_price = min(price_list)
                routes = []
                for i in range(data_len):
                    if data[i]["price"] == min_price:
                        link = data[i]["deep_link"]
                        route = data[i]['route']
                        for j in range(len(route)):
                            routes.append(
                                [route[j]["cityFrom"], route[j]["cityTo"]])
                        result = [min_price, routes, link, data_len]
                        break
            except (IndexError, ValueError):
                return None
            else:
                return result


async def next_step(update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs):
    """This Fuction iterates through the user data asks user for info if data is None
    This function will also iniate the flight search and provide the result to the user.
    """
    chat_id = update.effective_chat.id

    if context.user_data['flight_type'] == "ONEWAY" or context.user_data['flight_type'] == "RETURN":
        for key, value in context.user_data.items():
            if value == None:
                if key == 'Departure Airport':
                    return await context.bot.send_message(chat_id=chat_id, text='🛫 Provide your <b>departure</b> city.', parse_mode=ParseMode.HTML)
                if key == 'Destination Airport':
                    return await context.bot.send_message(chat_id=chat_id, text='🛬 Please provide your <b>destination</b> city.', parse_mode=ParseMode.HTML)
                if key == 'Departure Date (Earliest)':
                    return await context.bot.send_message(chat_id=chat_id, text='📅 Please enter your <b>earliest</b> departure date. e.g Day/Month/Year', parse_mode=ParseMode.HTML)
                if key == 'Departure Date (Latest)':
                    return await context.bot.send_message(chat_id=chat_id, text='📅 Please enter your <b>latest</b> departure date. e.g Day/Month/Year', parse_mode=ParseMode.HTML)
                if key == 'Minimum Lenth Of Stay':
                    return await context.bot.send_message(chat_id=chat_id, text='🏨 Please enter your <b>minimum</b> length of stay.', parse_mode=ParseMode.HTML)
                if key == 'Maximum Lenth Of Stay':
                    return await context.bot.send_message(chat_id=chat_id, text='🏨 Please enter your <b>maximum</b> length of stay.', parse_mode=ParseMode.HTML)
                if key == 'How Many Adults':
                    possible_adults = adults_menu()
                    return await context.bot.send_message(chat_id=chat_id, text='👪 How many adults?', reply_markup=possible_adults)
    elif context.user_data['flight_type'] == "MULTI-CITY":
        for key, value in context.user_data.items():
            if value == None:
                if key == 'Departure Airport':
                    return await context.bot.send_message(chat_id=chat_id, text='🛫 Provide your <b>departure</b> city.', parse_mode=ParseMode.HTML)
                if key == 'Destination Airport':
                    return await context.bot.send_message(chat_id=chat_id, text='🛬 Please provide your <b>destination</b> city.', parse_mode=ParseMode.HTML)
                if key == 'date_from':
                    return await context.bot.send_message(chat_id=chat_id, text='📅 Please enter your departure date. e.g Day/Month/Year')
                if key == 'How Many Adults':
                    possible_adults = adults_menu()
                    return await context.bot.send_message(chat_id=chat_id, text='👪 How many adults?', reply_markup=possible_adults)

    # This checks if all data has been fullfilled and iniates flight search and send out result - NOT FOR MULTI-CITY.
    if context.user_data['How Many Adults'] != None and context.user_data['flight_type'] == 'ONEWAY' or context.user_data['flight_type'] == 'RETURN':
        await context.bot.send_message(chat_id=chat_id, text='🤖 Okay, give me a sec. Searching for flights... 🔎')
        result = await search_flights(user_data=context.user_data)
        if result == False:
            await context.bot.send_message(chat_id=chat_id, text='🤖 looks like something went wrong, sorry. Please try again later.', reply_markup=main_menu_redirect)
        elif result == None:
            await context.bot.send_message(chat_id=chat_id, text='🤖 Sorry, no flights found at this moment. Try again later.', reply_markup=main_menu_redirect)
        else:
            reply = f'<b>Cheapest Flight Found!</b>\n\n🔎 Searched through {result[4]} flight results.\n\n📍 <b>Route:</b>\n\n✈️ {result[3].capitalize()} ➡️ {result[2].capitalize()}\n\n❗<b>Flight Type:</b> {context.user_data["flight_type"]}\n\n💵 <b>Cheapest Price:</b> R{result[0]}\n\nTravel dates and airports may have changed! Click on the link below to view the exact dates, airports, and duration of travel. 👇'
            link = flight_result_menu(link=result[1])
            # Save link and price to temp data to access for other functions
            context.user_data['link'] = result[1]
            context.user_data['price'] = result[0]
            await context.bot.send_message(chat_id=chat_id, text=reply, reply_markup=link, parse_mode=ParseMode.HTML)

    # This sends out the list of flight/ flights that the user stacks for multi city search
    if context.user_data['How Many Adults'] != None and context.user_data['flight_type'] == 'MULTI-CITY' and 'MT_result' not in kwargs:
        flight_list: list = context.user_data['requests']
        request = {
            "fly_to": context.user_data['Destination Airport'],
            "fly_from": context.user_data['Departure Airport'],
            "date_from": context.user_data['date_from'],
            "adults": context.user_data['How Many Adults']
        }
        flight_list.append(request)
        replies = []
        for i in flight_list:
            item = f"✈️ Flight From: {i['fly_from']} to {i['fly_to']}\n📅Date: {i['date_from']}\n\n"
            replies.append(item)
        response = ''.join(replies)
        await context.bot.send_message(chat_id=chat_id, text=response, reply_markup=multicity_menu, parse_mode=ParseMode.HTML)

    # This will send out result for Multi-city search
    if "MT_result" in kwargs:
        if kwargs['MT_result']:
            await context.bot.send_message(chat_id=chat_id, text='🤖 Okay, give me a sec. Searching for flights... 🔎')
            result = await search_flights(user_data=context.user_data)
            if result == False:
                await context.bot.send_message(chat_id=chat_id, text='🤖 looks like something went wrong, sorry. Please try again later.', reply_markup=main_menu_redirect)
            elif result == None:
                await context.bot.send_message(chat_id=chat_id, text='🤖 Sorry, no flights found at this moment. Try again later.', reply_markup=main_menu_redirect)
            else:
                routes = []
                for k in result[1]:
                    route = f'✈️ {k[0]} ➡️ {k[1]}\n'
                    routes.append(route)
                routes_formated = ''.join(routes)
                reply = f"<b>Cheapest Flight Found!</b>\n\n🔎 Searched through {result[3]} flight results.\n\n📍 <b>Route:</b>\n\n{routes_formated}\n\n❗<b>Flight Type:</b> {context.user_data['flight_type']}\n\n💵 <b>Cheapest Price:</b> R{result[0]}\n\nTravel dates and airports may have changed! Click on the link below to view the exact dates, airports, and duration of travel. 👇"
                link_menu = flight_result_menu(link=result[2])
                # Save link and price to temp data to access for other functions
                context.user_data['link'] = result[2]
                context.user_data['price'] = result[0]
                await context.bot.send_message(chat_id=chat_id, text=reply, reply_markup=link_menu, parse_mode=ParseMode.HTML)


def calc_percentage(old_p, new_p):
    """This function takes two arguments old_p == old price and new_p == new price. This will calculate the percentage in the price drop"""
    percentage = ((old_p - new_p) / old_p) * 100
    if percentage < 1:
        return round(percentage, 2)
    else:
        return round(percentage)
