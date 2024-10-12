# MESSAGE HANDLER

from telegram import Update
from telegram.ext import ContextTypes
from utils.database import DB
from utils.decorators import verify_user_on_del_alert

# KEY BOARD IMPORTS
from utils.keyboards import main_menu


@verify_user_on_del_alert
async def del_flight_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function is a Telegram Bot Message Handler.
    It is invoked when the user types a message that starts with '/TAP_DELETE_ID_'.
    The function will delete the flight alert with the id specified in the message.
    If the flight alert does not exist, it will send a message to the user with a red flag emoji and a message stating that the flight alert does not exist.
    If the flight alert exists, it will delete the flight alert and send a message to the user with a green checkmark emoji and a message stating that the flight alert has been deleted.
    The function will also close the database connection.
    """

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
