from bot_config import TelegramBot
import config


if __name__ == '__main__':
    bot = TelegramBot(username=config.BOT_USERNAME, token=config.BOT_TOKEN)
