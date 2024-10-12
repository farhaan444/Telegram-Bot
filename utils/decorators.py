from functools import wraps
from utils.database import DB
import config

# KEY BOARD IMPORTS
from utils.keyboards import single_button, main_menu_redirect


def send_action(action):
    """
    Decorator that will send a ChatAction to the user before the function is called.
    
    Args:
        action (str): The action to be sent. See https://core.telegram.org/bots/api#sendchataction
    
    Returns:
        function: The decorated function.
    """

    def wrapped(func):
        @wraps(func)
        async def bot_action(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)
            return await func(update, context, *args, **kwargs)
        return bot_action
    return wrapped


def verify_user_on_del_alert(func):
    """
    Decorator that verifies if the user is allowed to delete a flight alert based on the chat_id.
    
    The function checks if the chat_id of the user is the same as the chat_id associated with the flight alert.
    If the chat_id does not match, the function will send a message to the user with a red flag emoji and a message stating that the user is not allowed to do this.
    If the chat_id matches, the function will call the decorated function.
    """
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        chat_id = update.effective_chat.id
        flight_alert_id = int(update.message.text.split('ID_')[1].strip())
        db = DB()
        db_chat_id = db.cursor.execute(
            'SELECT chat_id FROM flight_data WHERE id = ?', (flight_alert_id,)).fetchone()
        db.close()

        if db_chat_id is None:
            return await func(update, context, *args, **kwargs)
        elif db_chat_id[0] == chat_id:
            return await func(update, context, *args, **kwargs)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='❗Sorry, you are not allowed to do this!', reply_markup=main_menu_redirect)
            return
    return wrapped


def check_save_alert_limit(func):
    """
    Decorator that checks if the user is allowed to save a flight alert based on the global setting of flight alert limit.
    
    The function checks if the chat_id of the user has already reached the global setting of flight alert limit.
    If the number of flight alerts have not reached the limit, the function will call the decorated function.
    If the number of flight alerts has reached the limit, the function will send a message to the user with a red flag emoji and a message stating that the user is not allowed to do this. The function will also provide a button for the user to manage their flight alerts.
    """
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        callback = update.callback_query
        await callback.answer()
        callback_data = callback.data
        chat_id = update.effective_chat.id
        db = DB()

        if callback_data != "track_flight":
            return await func(update, context, *args, **kwargs)
        elif callback_data == 'track_flight':
            ft_limit = db.cursor.execute('SELECT flight_alert_limit FROM global_settings').fetchone()[0]
            if ft_limit != 0:
                flight_data = db.cursor.execute(
                    'SELECT * FROM flight_data WHERE chat_id = ?', (chat_id,)).fetchall()
                alerts = len(flight_data)
                db.close()
                if alerts < ft_limit:
                    return await func(update, context, *args, **kwargs)
                else:
                    button = single_button(
                        text='🔔 Manage flight alerts', callback_data='get_flight_alerts')
                    return await context.bot.send_message(chat_id=chat_id, text=f'❗Only {file["FT_LIMIT"]} flights alert are allowed to be tracked at this time.', reply_markup=button)
            else:
                return await func(update, context, *args, **kwargs)
    return wrapped

def admin_only(func):
    """
    Decorator that checks if the user is an administrator. If the user is an administrator, the function will call the decorated function. If the user is not an administrator, the function will send a message to the user with a red flag emoji and a message stating that the user is not allowed to do this. The function will also provide a button for the user to return to the main menu.
    """
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        chat_id = update.effective_chat.id
        if chat_id in config.ADMINISTRATORS:
            return await func(update, context, *args, **kwargs)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='❗Sorry, Access Denied!', reply_markup=main_menu_redirect)
    return wrapped
