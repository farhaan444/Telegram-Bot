import logging
import tracemalloc
import warnings
import config
from telegram.warnings import PTBDeprecationWarning
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from utils.jobs import flight_search_job

# COMMAND IMPORTS
from handlers.start import start
from handlers.button import button
from handlers.conversation import converstaion
from handlers.unknown import unknown_commands
from handlers.flight_alerts import flight_alerts


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
        self.app.add_handler(CommandHandler(
            command='flight_alerts', callback=flight_alerts))

        # CALLBACK QUERY HANDLERS
        self.app.add_handler(CallbackQueryHandler(callback=button))

        # MESSAGE HANDLERS
        self.app.add_handler(MessageHandler(
            callback=unknown_commands, filters=filters.COMMAND))
        self.app.add_handler(MessageHandler(
            callback=converstaion, filters=filters.TEXT))

        # JOBS
        self.job_queue = self.app.job_queue
        self.job_3_hour = self.job_queue.run_repeating(
            callback=flight_search_job, interval=config.JOB_INTERVAL, first=config.FIRST_RUN)

        # RUN BUILD
        self.check_memory()
        self.app.run_polling()

    def check_memory(self):
        """Telegram bot documentation requires to check for memory issues/leaks in the bot."""
        tracemalloc.start()
