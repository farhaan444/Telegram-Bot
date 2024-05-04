# MESSAGE HANDLER

import config
from telegram import Update
from telegram.ext import ContextTypes
from utils.database import DB
from utils.decorators import verify_user_on_del_alert

# KEY BOARD IMPORTS
from utils.keyboards import main_menu


@verify_user_on_del_alert
async def del_flight_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function will delete the a flight data alert from the database.
    It uses the context.args to get the flight_data id from the command send to the user."""
    flight_alert_id = int(update.message.text.split('ID_')[1].strip())
    db = DB()

    try:
        flight_alert = db.cursor.execute(
            'SELECT * FROM flight_data WHERE id =?', (flight_alert_id,)).fetchone()
        if flight_alert is None:
            raise Exception()
        else:
            db.del_flight_data(id=flight_alert_id)
    except Exception:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='❗Flight alert already deleted.', reply_markup=main_menu)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='✅ Flight alert deleted.', reply_markup=main_menu)
    finally:
        db.close()
