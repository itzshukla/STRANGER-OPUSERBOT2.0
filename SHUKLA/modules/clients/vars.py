import os

from os import getenv
from dotenv import load_dotenv
from pyrogram import filters


if os.path.exists("Internal"):
  load_dotenv("Internal")


class Config(object):
    # REQUIRED VARIABLES
    API_ID = int(getenv("API_ID", 0))
    API_HASH = getenv("API_HASH", None)
    BOT_TOKEN = getenv("BOT_TOKEN", None)
    STRING_SESSION = getenv("STRING_SESSION", None)
    OWNER_ID = int(getenv("OWNER_ID", "8016771632"))
    MONGO_DATABASE = getenv("MONGO_DATABASE", None)
    OWNER_USERNAME = getenv("OWNER_USERNAME", None)
  
    SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6919199044").split()))
  
    # OPTIONAL VARIABLES
    SESSION_STRING = getenv("SESSION_STRING", None)
    COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", ". ! > *").split())
    USERBOT_PICTURE = getenv("USERBOT_PICTURE", "https://files.catbox.moe/23pqoe.jpg")
    LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0))

    # PM PERMIT 
    PM_GUARD = bool(getenv("PM_GUARD", True))
    PM_GUARD_TEXT = getenv("PM_GUARD_TEXT", "**🥀 ʜᴇʏ, ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ & ꜱᴜᴘᴇʀꜰᴀꜱᴛ ʜɪɢʜ Qᴜᴀʟɪᴛʏ ᴜꜱᴇʀʙᴏᴛ ᴀꜱꜱɪꜱᴛᴀɴᴛ ᴡɪᴛʜ ᴀɴ ᴜᴘɢʀᴀᴅᴇᴅ ᴠᴇʀꜱɪᴏɴ ꜱᴇᴄᴜʀɪᴛʏ ꜱʏꜱᴛᴇᴍ.\n\n🌿 ɪ ᴄᴀɴ'ᴛ ʟᴇᴛ ʏᴏᴜ ᴍᴇꜱꜱᴀɢᴇ ᴍʏ ᴏᴡɴᴇʀ'ꜱ ᴅᴍ ᴡɪᴛʜᴏᴜᴛ ᴍʏ ᴏᴡɴᴇʀ'ꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴ.\n\n❤️ ᴍʏ ᴏᴡɴᴇʀ ɪꜱ ᴏꜰꜰʟɪɴᴇ ɴᴏᴡ, ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴍʏ ᴏᴡɴᴇʀ ᴀʟʟᴏᴡꜱ ʏᴏᴜ.\n\n🍂 ᴘʟᴇᴀꜱᴇ ᴅᴏɴ'ᴛ ꜱᴘᴀᴍ ʜᴇʀᴇ, ʙᴇᴄᴀᴜꜱᴇ ꜱᴘᴀᴍᴍɪɴɢ ᴡɪʟʟ ꜰᴏʀᴄᴇ ᴍᴇ ᴛᴏ ʙʟᴏᴄᴋ ʏᴏᴜ ꜰʀᴏᴍ ᴍʏ ᴏᴡɴᴇʀ ɪᴅ 👍🏻**")
    PM_GUARD_LIMIT = int(getenv("PM_GUARD_LIMIT", 5))
  
  
    # do not edit these variables
    COMMAND_HANDLERS = []
    PLUGINS = {}
    FLOODXD = {}
    OLD_MSG = {}
    SUPUSER = filters.me
    SUDOERS = filters.user([])
    CRAIDUB = filters.user([])
    LRAIDUB = filters.user([])
    RRAIDUB = filters.user([])
    GBANSUB = filters.user([])
    GMUTEUB = filters.user([])
    #######################################
    for x in COMMAND_PREFIXES:
        COMMAND_HANDLERS.append(x)
    COMMAND_HANDLERS.append('')
    #######################################


# get all config variables in a list
all_vars = [i for i in Config.__dict__.keys()]
all_vals = [i for i in Config.__dict__.values()]