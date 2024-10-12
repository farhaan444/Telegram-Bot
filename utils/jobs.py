# Job Queue Functions
# You cannot use parse Update class in a job callback function as the Jobqueue is only expecting context
# If you need to use the Update class you would need to run the scheduler in the same function as context.job_queue.function(callback, 60, data=name, chat_id=chat_id)

from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from utils.database import DB
from utils.flight_search import is_date_in_past, search_flights, calc_percentage
import json

# KEY BOARD IMPORTS
from utils.keyboards import flight_alert_menu, main_menu_redirect


async def flight_search_job(context: ContextTypes.DEFAULT_TYPE):
    """
    This is a Telegram Bot Job Queue function.
    It is invoked by the scheduler in main.py.
    The function will check all the flight data in the database and check if the flight date is in the past.
    If the flight date is in the past, the function will delete the flight data from the database.
    If the flight date is not in the past, the function will search for flights using the data from the database and compare the price with the current price.
    If the current price is lower than the price in the database, the function will update the price in the database and send a message to the user with the price drop percentage and the new price.
    """
    
    db = DB()

    flight_data = db.cursor.execute('SELECT * FROM flight_data').fetchall()

    if flight_data != []:
        for i in flight_data:
            if i[10] == "ONEWAY" or i[10] == "RETURN":
                if is_date_in_past(date=i[4]) and is_date_in_past(date=i[5]):
                    user_flight_data = {
                        'Departure Airport': i[2],
                        'Destination Airport': i[3],
                        'Departure Date (Earliest)': i[4],
                        'Departure Date (Latest)': i[5],
                        'Minimum Lenth Of Stay': i[6],
                        'Maximum Lenth Of Stay': i[7],
                        'How Many Adults': i[8],
                        'currency': i[9],
                        'flight_type': i[10],
                    }
                    result = await search_flights(user_data=user_flight_data)
                    if result == None or result == False:
                        continue
                    else:
                        if result[0] < i[11]:
                            percentage = calc_percentage(
                                old_p=i[11], new_p=result[0])
                            db.update_flight_data(
                                id=i[0], price=result[0], data="current_price")
                            response = f'🔻<b>{percentage}% PRICE DROP ON YOUR FLIGHT ALERT</b>🔻\n\n🔔 <b>Your Price alert</b>:\n✈️ {i[2]} ➡️ {i[3]}\n📅 {i[4]} - {i[5]}\n💵 <b>Price before</b>: <s>R{i[11]}</s>\n\n⬇️ <b>PRICE DROPPED TO</b> R{result[0]}\n\nTravel dates and airports may have changed! Click on the link below to view the exact dates, airports, and duration of travel. 👇'
                            menu = flight_alert_menu(link=result[1])
                            await context.bot.send_message(chat_id=i[1], text=response, reply_markup=menu, parse_mode=ParseMode.HTML)
                else:
                    # notify user that the dates in flight data is in the past and data will be deleted.
                    response = f'❗<b>FLIGHT ALERT EXPIRED</b>❗\n\nThe flight alert below has expired and has been deleted.\n❗<b>Flight Type:</b> {i[10]}\n{i[2]}-{i[3]}\n{i[4]}-{i[5]}\n💵 <b>Price</b>: {i[11]}'
                    await context.bot.send_message(chat_id=i[1], text=response, reply_markup=main_menu_redirect, parse_mode=ParseMode.HTML)
                    db.del_flight_data(id=i[0])
            elif i[10] == "MULTI-CITY":
                multi_routes = json.loads(i[12])
                if is_date_in_past(date=multi_routes[0]["date_from"]):
                    user_flight_data = {
                        "requests": multi_routes,
                        "flight_type": i[10],
                        "currency": i[9],
                    }
                    result = await search_flights(user_data=user_flight_data)
                    if result == None or result == False:
                        continue
                    else:
                        if result[0] < i[11]:
                            percentage = calc_percentage(
                                old_p=i[11], new_p=result[0])
                            db.update_flight_data(
                                id=i[0], price=result[0], data="current_price")
                            routes = []
                            for j in multi_routes:
                                route = f"✈️ ({j['fly_from']} ➡️ {j['fly_to']} - {j['date_from']})\n"
                                routes.append(route)
                            routes_formated = ''.join(routes)
                            response = f'🔻<b>{percentage}% PRICE DROP ON YOUR FLIGHT ALERT</b>🔻\n\n🔔 <b>Your Price alert</b>:\n{routes_formated}💵 <b>Price before</b>: <s>R{i[11]}</s>\n\n⬇️ <b>PRICE DROPPED TO</b> R{result[0]}\n\nTravel dates and airports may have changed! Click on the link below to view the exact dates, airports, and duration of travel. 👇'
                            menu = flight_alert_menu(link=result[2])
                            await context.bot.send_message(chat_id=i[1], text=response, reply_markup=menu, parse_mode=ParseMode.HTML)
                else:
                    # notify user that the dates in flight data is in the past and data will be deleted.
                    multi_routes = json.loads(i[12])
                    routes = []
                    for j in multi_routes:
                        route = f"({j['fly_from']} - {j['fly_to']} - {j['date_from']})\n"
                        routes.append(route)
                    routes_formated = ''.join(routes)
                    response = f'❗<b>FLIGHT ALERT EXPIRED</b>❗\n\nThe flight alert below has expired and has been deleted.\n❗<b>Flight Type:</b> {i[10]}\n{routes_formated}💵 <b>Price</b>: {i[11]}'
                    await context.bot.send_message(chat_id=i[1], text=response, reply_markup=main_menu_redirect, parse_mode=ParseMode.HTML)
                    db.del_flight_data(id=i[0])
    else:
        db.close()

    # close db after job executes successfully.
    db.close()
