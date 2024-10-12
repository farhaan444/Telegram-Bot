import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from utils.jobs import flight_search_job
from utils.database import DB

# Filters 
from utils.filters import Admin_convo_filter

# HANDLER IMPORTS
from handlers.start import start
from handlers.button import button
from handlers.conversation import converstaion
from handlers.unknown import unknown_commands
from handlers.flight_alerts import flight_alerts
from handlers.del_flight_alert import del_flight_alert
from handlers.flight_search_reset import flight_search_reset
from handlers.error import errors
from handlers.main_menu import handler_main_menu
from handlers.help import help
from handlers.admin import admin_dashboard, admin_convo


class TelegramBot:
    """
    This class is a Telegram Bot. It contains the entire logic required to run a Telegram Bot.
    It includes the Telegram Bot token, command handlers, callback query handlers, message handlers, error handlers, and job queue.
    """

    def __init__(self, token: str) -> None:
        # TELEGRAM BOT FATHER CREDENTIALS
        self.token = token

        # LOGGING
        self.console_logger = logging.basicConfig(  # Global logger --> Print to console
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger()
        self.logger.setLevel(level=logging.INFO)
        self.httpx_logger = logging.getLogger("httpx")
        self.httpx_logger.setLevel(level=logging.WARNING)
        # LOGGING GLOBAL FORMAT
        self.log_gformat = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # LOG HANDLERS
        self.global_log_handler = logging.FileHandler(
            filename=r"Logs/global.log")
        self.global_log_handler.setFormatter(self.log_gformat)
        self.global_log_handler.setLevel(logging.INFO)

        self.exception_handler = logging.FileHandler(
            filename=r"Logs/exceptions.log")
        self.exception_handler.setFormatter(self.log_gformat)
        self.exception_handler.setLevel(logging.ERROR)

        # ADD HANDLERS TO LOGGERS
        self.logger.addHandler(self.global_log_handler)
        self.logger.addHandler(self.exception_handler)
        self.httpx_logger.addHandler(self.global_log_handler)

        # APP BUILD
        self.app = ApplicationBuilder().token(
            token=self.token).concurrent_updates(True).build()
        
        # Init Custom Filters 
        self.admin_convo_filter = Admin_convo_filter(chat_data=self.app.chat_data)

        # COMMAND HANDLERS
        self.app.add_handler(CommandHandler(command='start', callback=start))
        self.app.add_handler(CommandHandler(
            command='flight_alerts', callback=flight_alerts))
        self.app.add_handler(CommandHandler(
            command='reset', callback=flight_search_reset))
        self.app.add_handler(CommandHandler(
            command="menu", callback=handler_main_menu))
        self.app.add_handler(CommandHandler(command="help", callback=help))
        self.app.add_handler(CommandHandler(command='admin', callback=admin_dashboard))

        # CALLBACK QUERY HANDLERS
        self.app.add_handler(CallbackQueryHandler(callback=button))

        # MESSAGE HANDLERS - ORDER SENSITIVE
        self.app.add_handler(MessageHandler(
            callback=del_flight_alert, filters=filters.Regex(r'TAP_DELETE_ID_')))
        self.app.add_handler(MessageHandler(
            callback=unknown_commands, filters=filters.COMMAND))
        self.app.add_handler(MessageHandler(callback=admin_convo, filters=self.admin_convo_filter))
        self.app.add_handler(MessageHandler(
            callback=converstaion, filters=filters.TEXT))

        # ERROR HANDLERS
        self.app.add_error_handler(callback=errors)

        # JOBS
        self.job_queue = self.app.job_queue
        self.job_3_hour = self.job_queue.run_repeating(
            callback=flight_search_job, interval=self.load_global_settings()['FS_JOB_INTV'], first=900)

        # RUN BUILD
        self.app.run_polling(timeout=60)

    
    def load_global_settings(self):

        """
        This method loads the global settings from the database.
        The global settings that are loaded are the flight search job interval.

        Returns:
            dict: A dictionary containing the global settings.
        """
        db = DB()
        settings = {}

        settings['FS_JOB_INTV'] = db.cursor.execute('SELECT fs_job_interval FROM global_settings').fetchone()[0]

        db.close()
        return settings
