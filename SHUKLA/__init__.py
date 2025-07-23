import os

from .console import LOGGER
from .modules.clients.clients import Shukla
from .modules.clients.vars import Config
from .modules.clients.command import *

__version__ = "v2.0.1"

if Config.API_ID == 0:
    LOGGER.error("API_ID is missing! Kindly check again!")
    exit()
if not Config.API_HASH:
    LOGGER.error("API_HASH is missing! Kindly check again!")
    exit()
if not Config.BOT_TOKEN:
    LOGGER.error("BOT_TOKEN is missing! Kindly check again!")
    exit()
if not Config.STRING_SESSION:
    LOGGER.error("STRING_SESSION is missing! Kindly check again!")
    exit()
if not Config.MONGO_DATABASE:
    LOGGER.error("DATABASE_URL is missing! Kindly check again!")
    exit()
if Config.LOG_GROUP_ID == 0:
    LOGGER.error("LOG_GROUP_ID is missing! Kindly check again!")
    exit()

for file in os.listdir():
    if file.endswith(".session"):
        os.remove(file)
for file in os.listdir():
    if file.endswith(".session-journal"):
        os.remove(file)


shukla = Shukla()
app = shukla.app
bot = shukla.bot
call = shukla.call
log = LOGGER
var = Config()

db = {}
flood = {}
OLD_MSG = {}
spam_chats = []

cdx = commandx
cdz = commandz


PLUGINS = var.PLUGINS
SUPUSER = var.SUPUSER
SUDOERS = var.SUDOERS
OWNER_ID = Config.OWNER_ID
SUDO_USER = Config.SUDO_USERS
OWNER_USERNAME = Config.OWNER_USERNAME
Config.SUDO_USERS.append(Config.OWNER_ID)


from .modules.clients.command import eor
eor = eor

from .modules.helpers.wrapper import (
    super_user_only, sudo_users_only
)

from .modules.clients.vars import Config
vars = Config