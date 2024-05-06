import os
from dotenv import load_dotenv

load_dotenv()

# BOT CREDENTIALS PROVIDED BY BOT FATHER
BOT_TOKEN: str = os.getenv('BOT_TOKEN')

# KIWI CREDENTIALS  FLIGHT API
KIWI_API_KEY_STD: str = os.getenv('KIWI_API_KEY_STD')
KIWI_API_KEY_MULTICITY: str = os.getenv('KIWI_API_KEY_MULTICITY')

# DATABASE FILES
DATABASE_PATH: str = os.getenv('DATABASE_PATH')

# USER TYPES
ADMINISTRATORS: list = os.getenv('ADMINISTRATORS')

# JOB SCHEDULING INTERVALS - SECONDS
FIRST_RUN_FS = int(os.getenv('FIRST_RUN_FS'))
JOB_INTERVAL_FS = int(os.getenv('JOB_INTERVAL_FS'))

# FLIGHT TRACKING LIMITS - SET TO 0 FOR UNNLIMITED FLIGHT ALERTS
FT_LIMIT = int(os.getenv('FT_LIMIT'))
