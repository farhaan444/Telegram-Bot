# ERROR HANDLER

from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)


async def errors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Error handler that handles bot errors and prints out errors to console """
    logger.exception(context.error)
