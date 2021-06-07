import os
import time

class Config(object):
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    # Get these values from my.telegram.org
    # Array to store users who are authorized to use the bot
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    # Banned Unwanted Members..
    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # chunk size that should be used with requests
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    # default thumbnail to be used in the videos
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90")
    # proxy for accessing youtube-dl in GeoRestricted Areas
    # Get your own proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    AUTH_CHANNEL = "@Super_botz"
    AUTH_CHANNEL_URL = "https://t.me/Super_botz"
    BOT_START_TIME = time.time()
    TG_MAX_FILE_SIZE = 2097152000
    DEF_WATER_MARK_FILE = ""
    ONE_BY_ONE = []
    TODAY_USERS = []
    myclient = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.uwnjv.mongodb.net/<dbname>?retryWrites=true&w=majority")
    mydb = myclient["mydatabase"]
    BANNED = mydb["banned"]
