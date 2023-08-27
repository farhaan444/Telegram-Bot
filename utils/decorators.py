from functools import wraps
from utils.database import DB
import config

# KEY BOARD IMPORTS
from utils.keyboards import single_button


def send_action(action):
    """This decorator send a tryping chat action to the user when the bot is handling a request.
    action = ChatAction Constant"""

    def wrapped(func):
        @wraps(func)
        async def bot_action(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)
            return await func(update, context, *args, **kwargs)
        return bot_action
    return wrapped


def verify_user_on_del_alert(func):
    """This decorator verifies if the actual user iniated the del_flight_command.
    Imposters can type the link command and try to delete."""
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        chat_id = update.effective_chat.id
        flight_alert_id = int(update.message.text.split('ID_')[1].strip())
        db = DB(file=config.DATABASE_PATH)
        db_chat_id = db.cursor.execute(
            'SELECT chat_id FROM flight_data WHERE id = ?', (flight_alert_id,)).fetchone()
        db.close()

        if db_chat_id is None:
            return await func(update, context, *args, **kwargs)
        elif db_chat_id[0] == chat_id:
            return await func(update, context, *args, **kwargs)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='❗Sorry, you are not allowed to do this!')
            return
    return wrapped


def check_save_alert_limit(func):
    """This decorator checks if the user has reached the tracked flight alert limit."""
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        callback = update.callback_query
        await callback.answer()
        callback_data = callback.data
        chat_id = update.effective_chat.id

        if callback_data != "track_flight":
            return await func(update, context, *args, **kwargs)
        elif callback_data == 'track_flight':
            db = DB(file=config.DATABASE_PATH)
            flight_data = db.cursor.execute(
                'SELECT * FROM flight_data WHERE chat_id = ?', (chat_id,)).fetchall()
            alerts = len(flight_data)
            db.close()
            if alerts < config.FT_LIMIT:
                return await func(update, context, *args, **kwargs)
            else:
                button = single_button(
                    text='🔔 Manage flight alerts', callback_data='get_flight_alerts')
                return await context.bot.send_message(chat_id=chat_id, text=f'❗Only {config.FT_LIMIT} flight alerts allowed at this time.', reply_markup=button)
    return wrapped
