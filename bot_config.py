import logging
import tracemalloc
import warnings
from telegram.warnings import PTBDeprecationWarning
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# COMMAND IMPORTS
from handlers.start import start
from handlers.button import button
from handlers.conversation import converstaion


# VERY IMPORTANT COMMENTS
# THIS IS HOW YOU CALL ANOTHER HANDLER FROM ONE HANDLER - PARAMETERS (update, context) ----> await self.func(update=update, context=context)


class TelegramBot:
    def __init__(self, username: str, token: str) -> None:
        # TELEGRAM BOT FATHER CREDENTIALS
        self.username = username
        self.token = token

        # LOGGING
        self.log = logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.dep_warning = warnings.filterwarnings(
            'error', category=PTBDeprecationWarning)
        # set this to only recieve errors/execptions --> comment/uncomment.
        self.log = logging.getLogger('httpx').setLevel(logging.WARNING)

        # APP BUILD
        self.app = ApplicationBuilder().token(token=self.token).build()

        # COMMAND HANDLERS
        self.app.add_handler(CommandHandler(command='start', callback=start))

        # CALLBACK QUERY HANDLERS
        self.app.add_handler(CallbackQueryHandler(callback=button))

        # MESSAGE HANDLERS
        self.app.add_handler(MessageHandler(
            callback=converstaion, filters=filters.TEXT))

        # RUN BUILD
        self.check_memory()
        self.app.run_polling()

    def check_memory(self):
        """Telegram bot documentation requires to check for memory issues/leaks in the bot."""
        tracemalloc.start()
