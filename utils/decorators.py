from functools import wraps


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
