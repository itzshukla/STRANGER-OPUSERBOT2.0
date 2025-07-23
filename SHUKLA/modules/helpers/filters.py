from .vars import Config
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import Update
from typing import Union, List, Dict, Optional


def commandx(commands: Union[str, List[str]]):
    return filters.command(commands, Config.COMMAND_PREFIXES)

def commandz(commands: Union[str, List[str]]):
    return filters.command(commands, Config.COMMAND_HANDLERS)