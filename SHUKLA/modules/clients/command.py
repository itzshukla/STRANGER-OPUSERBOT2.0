from .vars import Config
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import Update
from typing import Union, List, Dict, Optional


PREFIXES = Config.COMMAND_PREFIXES
HANDLERS = Config.COMMAND_HANDLERS

def commandx(commands: Union[str, List[str]]):
    return filters.command(commands, PREFIXES)

def commandz(commands: Union[str, List[str]]):
    return filters.command(commands, HANDLERS)


# Edit Message

async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    msg = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await msg(*args, **kwargs)

eor = edit_or_reply