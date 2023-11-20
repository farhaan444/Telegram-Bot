# COMMAND HANDLER

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from utils.database import DB
import config

# KEY BOARD IMPORTS
from utils.keyboards import main_menu_redirect, delete_all_menu


async def flight_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function returns all the saved flight alerts that are been tracked in the database.
    It will provide a link to delete each a flight alert."""
    db = DB(file=config.DATABASE_PATH)
    chat_id = update.effective_chat.id

    alert_data = db.cursor.execute(
        'SELECT * FROM flight_data WHERE chat_id = ?', (chat_id,)).fetchall()

    db.close()

    if alert_data == []:
        await context.bot.send_message(chat_id=chat_id, text='You have no flight alerts yet. Start a flight search and create a new flight alert.', reply_markup=main_menu_redirect)
    else:
        alerts = []
        for i in alert_data:
            alert = f'<b>Location</b>: {i[2]} - {i[3]}\n<b>Dates</b>: {i[4]} - {i[5]}\n<b>Adults</b>: {i[8]}\n<b>Flight Type</b>: {i[10]}\n<b>Price</b>: R{i[11]}\n<b>Delete flight alert</b>: /TAP_DELETE_ID_{i[0]}\n\n'
            alerts.append(alert)
        response = ''
        response = response.join(alerts)
        menu = delete_all_menu()
        await context.bot.send_message(chat_id=chat_id, text=response, reply_markup=menu, parse_mode=ParseMode.HTML)
