import logging
import tracemalloc
import warnings
import config
from telegram.warnings import PTBDeprecationWarning
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from utils.jobs import flight_search_job

# HANDLER IMPORTS
from handlers.start import start
from handlers.button import button
from handlers.conversation import converstaion
from handlers.unknown import unknown_commands
from handlers.flight_alerts import flight_alerts
from handlers.del_flight_alert import del_flight_alert
from handlers.flight_search_reset import flight_search_reset
from handlers.error import errors


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
        self.app = ApplicationBuilder().token(
            token=self.token).concurrent_updates(True).build()

        # COMMAND HANDLERS
        self.app.add_handler(CommandHandler(command='start', callback=start))
        self.app.add_handler(CommandHandler(
            command='flight_alerts', callback=flight_alerts))
        self.app.add_handler(CommandHandler(
            command='reset', callback=flight_search_reset))

        # CALLBACK QUERY HANDLERS
        self.app.add_handler(CallbackQueryHandler(callback=button))

        # MESSAGE HANDLERS - ORDER SENSITIVE
        self.app.add_handler(MessageHandler(
            callback=del_flight_alert, filters=filters.Regex(r'TAP_DELETE_ID_')))
        self.app.add_handler(MessageHandler(
            callback=unknown_commands, filters=filters.COMMAND))
        self.app.add_handler(MessageHandler(
            callback=converstaion, filters=filters.TEXT))

        # ERROR HANDLERS
        self.app.add_error_handler(callback=errors)

        # JOBS
        self.job_queue = self.app.job_queue
        self.job_3_hour = self.job_queue.run_repeating(
            callback=flight_search_job, interval=config.JOB_INTERVAL_FS, first=config.FIRST_RUN_FS)

        # RUN BUILD
        self.app.run_polling(timeout=60)
