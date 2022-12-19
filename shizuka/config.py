# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
# A Powerful Music And Management Bot
# Property Of Rocks Indian Largest Chatting Group
# Without Credit (Mother Fucker)
# Roses are red, Violets are blue, A face like yours, Belongs in a zoo


import json
import os


def get_user_list(config, key):
    with open("{}/shizuka/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = "15599295"
    API_HASH = "4ce42998f7df4a64934294dadca28ae0"
    TOKEN = "5414076366:AAHM8PhG9SQBgwc6tAXS4SdXEkY4tdqThzI"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    STRING_SESSION = "1AZWarzUBu4OzXXVgrdfI-7W2-yRaq8uiMopQzK4hl08WqpwpmE4OFG4oPHGExhGW6UWUgoIH78Bbx2mavk2Jx_cT9qMzrx_xUb7BxVo2lgD6jU4-tON4MOy89VuzfUmbMOTLWveakEeaAcx7NhFPrn81rQNjodIdgDJoHmv6t_gee-n_1j6cWqCOy9AkImM09ORxsskpbzKcsgwWsPbi6lOCTXpJiRuLHufhXWBUu0QDxz176YaBHxYTWCWW_eIMCyXTrjJd5UTubSnGOVIu-RgicQNJknxRKnX4zl8_NHfydME37-n-3CPq3d5NFC8tBzaUTf3pkIoLFNcDui-hVcdjeScQf4k="
    OWNER_ID = "5608390546"  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "YoungFaiz"
    SUPPORT_CHAT = "ayrabots"  # Your own group for support, do not add the @
    BOT_NAME = ""
    UPDATES_CHANNEL = (
        "Ayraupdates"  # Your own channel for Updates of bot, Do not add @
    )
    JOIN_LOGGER = (
        "-1001621682412"
    )  # Prints any new group the bot is added to, prints just the name and ID.
    REM_BG_API_KEY = "http://removebg.com"
    TEMP_DOWNLOAD_DIRECTORY = "none"
    EVENT_LOGS = (
        "-1001621682412"
    )  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    SQLALCHEMY_DATABASE_URI = "postgres://zygsjawf:kzExgeliPA4GGwVWDlXySLXCDafJGxUZ@castor.db.elephantsql.com/zygsjawf"  # do you hub your old heroku app database_URL then put here, most use 25days ago sql
    LOAD = (
        []
    )  # try to kang this db ur big mothersfuckers i know your noob so only kanging my db
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = None
    INFOPIC = "https://telegra.ph/file/6eda47c03eaf8b8c26cc4.jpg"
    URL = None
    SPAMWATCH_API = "RxyUymWXR0cd9vD63D9JYS~RlRGpekPMC~IBSMHacCafhfeUbRtG~5EowuC2D_5H"  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"
    BOT_USERNAME = "MissAqsa_bot"
    MONGO_DB_URI = "mongodb+srv://its_star_boi:7234049299@cluster0.8twjh9e.mongodb.net/?retryWrites=true&w=majority"
    BOT_ID = "5414076366"

    DRAGONS = get_user_list("elevated_users.json", "sudos")

    DEV_USERS = get_user_list("elevated_users.json", "devs")
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = get_user_list("elevated_users.json", "supports")
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")
    DONATION_LINK = "https://t.me/its_star_boi"  # EG, paypal
    CERT_PATH = None
    PORT = "5000"
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = "True"
    STRICT_GMUTE = "True"
    WORKERS = (
        8  # Number of subthreads to use. Set as number of threads your processor uses
    )
    BAN_STICKER = ""  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    ARQ_API_URL = "https://thearq.tech"
    ARQ_API_KEY = "GKNOHX-UDSREJ-AWTSGO-XFDSCY-ARQ"
    CASH_API_KEY = (
        "awoo"  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "awoo"  # Get your API key from https://timezonedb.com/api
    OPENWEATHERMAP_ID = "awoo"
    WALL_API = (
        "awoo"  # For wallpapers, get one from https://wall.alphacoders.com/api.php
    )
    AI_API_KEY = "awoo"  # For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
