from ... import *
from SHUKLA.modules.clients.utils import *
from SHUKLA.modules.mongo.streams import *
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound
import logging

logger = logging.getLogger(__name__)

# Pause Stream (pause)
@app.on_message(commandz(["pause"]) & SUDOERS)
async def pause_stream(client, message):
    chat_id = message.chat.id
    try:
        queue = await db.get_queue(chat_id)
        if queue:
            await call.pause_stream(chat_id)
            await eor(message, "**⏸ Stream Paused!**")
        else:
            await eor(message, "**❌ Nothing Playing!**")
    except Exception as e:
        logger.error(f"❌ Error in pause_stream: {e}")
        await eor(message, f"**Error:** `{e}`")

# Pause Stream (cpause)
@app.on_message(cdz(["cpse", "cpause"]) & SUDOERS)
async def pause_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")
    try:
        a = await call.get_call(chat_id)
        if a.status == "playing":
            await call.pause_stream(chat_id)
            await eor(message, "**⏸ Stream Paused!**")
        elif a.status == "paused":
            await eor(message, "**⏸ Already Paused!**")
        elif a.status == "not_playing":
            await eor(message, "**❌ Nothing Streaming!**")
    except GroupCallNotFound:
        await eor(message, "**❌ I am Not in VC!**")
    except Exception as e:
        logger.error(f"❌ Error in cpause: {e}")
        await eor(message, f"**Error:** `{e}`")