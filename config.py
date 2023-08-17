import os
from dotenv import load_dotenv

load_dotenv()

# BOT CREDENTIALS PROVIDED BY BOT FATHER
BOT_USERNAME: str = os.getenv('BOT_USERNAME')
BOT_TOKEN: str = os.getenv('BOT_TOKEN')

# KIWI CREDENTIALS  FLIGHT API

KIWI_API_KEY: str = os.getenv('KIWI_API_KEY')
