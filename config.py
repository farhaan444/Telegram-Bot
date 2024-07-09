import os
from dotenv import load_dotenv
import ast

load_dotenv()

# BOT CREDENTIALS PROVIDED BY BOT FATHER
BOT_TOKEN: str = os.getenv('BOT_TOKEN')

# KIWI CREDENTIALS  FLIGHT API
KIWI_API_KEY_STD: str = os.getenv('KIWI_API_KEY_STD')
KIWI_API_KEY_MULTICITY: str = os.getenv('KIWI_API_KEY_MULTICITY')

# DATABASE FILES
DATABASE_PATH: str = os.getenv('DATABASE_PATH')

# USER TYPES
ADMINISTRATORS: list = ast.literal_eval(os.getenv('ADMINISTRATORS'))

