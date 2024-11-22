import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')

DATABASE_URL: str = os.getenv('DATABASE_URL')

NOTION_TOKEN = "ntn_H19956372347cmeOvTadcB7SaPT458iRhbnp8Dw99qx1xU"

NOTION_DATABASE_ID = "145076f3-01f2-8036-b6df-e04fed09cd82"

LOG_CHANNEL_ID: str = os.getenv('LOG_CHANNEL_ID')
