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

    API_ID = "8744937"
    API_HASH = "2f92b21f6c3ed48a7e1695fc5c21f63d"
    TOKEN = "5336039764:AAG7GcmSpWJlQjBn-aUaRnNLcbdoXZ-XuOc"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    STRING_SESSION = "1BVtsOL8Bu7SPTxygWyP0qGuauKPJdqFICFSUBx2A4mDC905VHviRrGld5yhhSD4iJ-jU1_wK1JiTMds83kUmp-tip9wAG539k7ejxWYSNJt1zRw_C3yrS7WC-BBnRBlU-_jUDx6flVsULZwu8CZbIGQj3Bg0Ox-ZknJ_BF1ivZZFP3U6vAfXI9NobCX4PaScv9c5Q6O03G5jnADo6FUogQCdUMDKnROcZY6s6Lkq2ig7lHmLiZmrEsXhbCP-Y83TMd4ifw_QLfvwL8fJ1zsYXwFUfZjPPnpnN_uCAzg3eOlConkseFSrzWaeVoi9PW7gxxwJJpkP-3Q94k3PYWuaO_T-oB6X3IY="
    OWNER_ID = "5463205082"  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "its_star_boi"
    SUPPORT_CHAT = "Best_Friendsafor_Ever"  # Your own group for support, do not add the @
    BOT_NAME = ""
    UPDATES_CHANNEL = (
        "Its_star_network"  # Your own channel for Updates of bot, Do not add @
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
    INFOPIC = "https://telegra.ph/file/2f6c4b784ee0977777e93.jpg"
    URL = None
    SPAMWATCH_API = "RxyUymWXR0cd9vD63D9JYS~RlRGpekPMC~IBSMHacCafhfeUbRtG~5EowuC2D_5H"  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"
    BOT_USERNAME = "itz_shizuka_robot"
    MONGO_DB_URI = "mongodb+srv://venomxspam097:a5t0d6w&@cluster0.zoh6lpb.mongodb.net/?retryWrites=true&w=majority"
    BOT_ID = "5336039764"

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
