from functools import wraps
from utils.database import DB
import config


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


def verify_user(func):
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
            await context.bot.send_message(chat_id=update.effective_chat.id, text='❗Unauthorzied access denied!')
            return
    return wrapped
