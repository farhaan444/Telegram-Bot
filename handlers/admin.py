# COMMAND HANDLER @ admin_dashboard
# MESSAGE HANDLER @ admin_convo

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
import json
from utils.database import DB
from telegram.constants import ParseMode
from utils.flight_search import validate_number, is_int_0


# DECORATOR IMPORTS
from utils.decorators import send_action, admin_only

# KEY BOARD IMPORTS
from utils.keyboards import admin_menu

@send_action(action=ChatAction.TYPING)
@admin_only
async def admin_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """
    This function is a Telegram Bot Command Handler.
    It is invoked when the user types /admin_dashboard in a Telegram chat.
    The function will return a message with various statistics about the bot to the user.
    The message includes the total number of users, the total number of flight alerts, the first run interval for the flight tracker job, the run intervals for the flight tracker job, and the flight alert limit.
    The message also includes a button to set the flight alert limit and a button to set the run intervals for the flight tracker job.
    """
    
    chat_id = update.effective_chat.id

    db = DB()
    USER_COUNT = len(db.cursor.execute('SELECT * FROM users').fetchall())
    FA_COUNT = len(db.cursor.execute('SELECT * FROM flight_data').fetchall())
    FA_LIMIT = db.cursor.execute('SELECT flight_alert_limit FROM global_settings').fetchone()[0]
    FS_JOB_INTV = db.cursor.execute('SELECT fs_job_interval FROM global_settings').fetchone()[0]
    db.close()

    reply = f"""
<b>🔐 Welcome To The Admin Dashboard.</b>
            
<b>USER DATA</b>
👫 Total Users: {USER_COUNT}
🔔 Tolal Flight Alerts: {FA_COUNT}

<b>JOBS</b>
<i>Flight Tracker Job</i>
⏲️ First Run Interval: 900 seconds.
⏲️ Run Intervals: {FS_JOB_INTV} seconds.

<b>Flight alert limit:</b> 
🖐️ Limit: {FA_LIMIT}

"""

    await context.bot.send_message(chat_id=chat_id, text=reply, reply_markup=admin_menu, parse_mode=ParseMode.HTML)


@send_action(action=ChatAction.TYPING)
async def admin_convo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """
    This function is a Telegram Bot Message Handler.
    It is invoked when the user sends a message during an admin session.
    The function will check what the user is trying to set, either the flight tracker job interval or the flight alert limit.
    The function will then validate the input and update the relevant value in the database.
    The function will then send a message to the user indicating if the update was successful or not.
    The function will also clear the chat_data to indicate that the admin session has expired.
    """
    
    chat_id = update.effective_chat.id
    TEXT = update.message.text.strip()
    db = DB()

    if context.chat_data['set'] == 'Set Flight Tracker Job':
        try:
            check_1 = validate_number(TEXT)
            if check_1 == False:
                raise TypeError
            check_2 = is_int_0(TEXT)
            if check_2 == True:
                raise ValueError
            if int(TEXT) < 900:
                raise Exception('below minimum')
        except TypeError:
                reply = '🤖 Sorry, please enter only a number. e.g 900'
                await context.bot.send_message(chat_id=chat_id, text=reply)
        except ValueError:
                reply = '🤖 Sorry, you cannot set job interval to 0 seconds. Please a number more than or equal to 900 seconds'
                await context.bot.send_message(chat_id=chat_id, text=reply)
        except Exception:
                reply = '🤖 Sorry, you can only set a minimum value of 900 seconds or more. Please enter a new number'
                await context.bot.send_message(chat_id=chat_id, text=reply)
        else:
            query = f'UPDATE global_settings SET fs_job_interval = ? WHERE id = 1'
            data = int(TEXT)
            db.cursor.execute(query, (data,))
            db.commit()
            await context.bot.send_message(chat_id=chat_id, text='🤖 Flight job interval has been updated.')
            await admin_dashboard(update=update, context=context)
            context.chat_data.clear() # VERY IMPORTANT TO CLEAR CHAT_DATA TO INDICATE ADMIN SESSION HAS EXPIRED.
        finally:
             db.close()
    elif context.chat_data['set'] == 'Set Flight Alert Limit':
        try:
            check_1 = validate_number(TEXT)
            if not check_1:
                raise TypeError
            if int(TEXT) < 0:
                raise Exception('Input below minimum')
        except TypeError:
                reply = '🤖 Sorry, please enter only a number. e.g 2'
                await context.bot.send_message(chat_id=chat_id, text=reply)
        except Exception:
                reply = '🤖 Sorry, you can only set a minimum value of less than 0. Please enter a new number'
                await context.bot.send_message(chat_id=chat_id, text=reply)
        else:
            query = f'UPDATE global_settings SET flight_alert_limit  = ? WHERE id = 1'
            data = int(TEXT)
            db.cursor.execute(query, (data,))
            db.commit()
            await context.bot.send_message(chat_id=chat_id, text='🤖 Flight alert limit has been updated.')
            await admin_dashboard(update=update, context=context)
            context.chat_data.clear() # VERY IMPORTANT TO CLEAR CHAT_DATA TO INDICATE ADMIN SESSION HAS EXPIRED. 
        finally:
             db.close()
