import os
from os import environ

API_ID = int(environ.get("API_ID", "22182189"))
API_HASH = environ.get("API_HASH", "5e7c4088f8e23d0ab61e29ae11960bf5")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

CREDIT = environ.get("CREDIT", "『ᴀᴅᴍɪɴ』")
TG_CHANNEL = environ.get("TG_CHANNEL", "https://t.me/Devfff_bot")

OWNER_ID = int(environ.get("OWNER_ID", "0"))
MONGO_URI = environ.get("MONGO_URI", "")
MONGO_DB_NAME = environ.get("MONGO_DB_NAME", "aura_bot")
