import os
from dotenv import load_dotenv

load_dotenv()

# BOT CREDENTIALS PROVIDED BY BOT FATHER
BOT_USERNAME: str = os.getenv('BOT_USERNAME')
BOT_TOKEN: str = os.getenv('BOT_TOKEN')

# KIWI CREDENTIALS  FLIGHT API
KIWI_API_KEY: str = os.getenv('KIWI_API_KEY')

# DATABASE FILES
DATABASE_PATH: str = os.getenv('DATABASE_PATH')

# USER TYPES
ADMINISTRATOR: str = os.getenv('ADMINISTRATOR')
MODERATOR: str = os.getenv('MODERATOR')
REGULAR_USER: str = os.getenv('REGULAR_USER')

# JOB SCHEDULING INTERVALS - SECONDS
FIRST_RUN_FS = int(os.getenv('FIRST_RUN_FS'))
JOB_INTERVAL_FS = int(os.getenv('JOB_INTERVAL_FS'))

# FLIGHT TRACKING LIMITS - SET TO 0 FOR UNNLIMITED FLIGHT ALERTS
FT_LIMIT = int(os.getenv('FT_LIMIT'))

# delete this comment
