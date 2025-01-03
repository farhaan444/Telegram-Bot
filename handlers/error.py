# ERROR HANDLER

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import logging
import datetime
import config

logger = logging.getLogger(__name__)


async def errors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Error handler for the telegram bot.
    
    This function is called when an exception is raised in any of the 
    command handlers or message handlers. It logs the exception and 
    sends a message to the administrators specified in the config.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.

    Returns:
        None
    """
    
    logger.exception(context.error)
    curr_datetime = datetime.datetime.now()
    error = context.error
    reply = f"{curr_datetime}\nA bot exception/error has occured. Please see logs.\n<b>Error: {error.__doc__}</b>"
    for i in config.ADMINISTRATORS:
        await context.bot.send_message(chat_id=i, text=reply, parse_mode=ParseMode.HTML)
