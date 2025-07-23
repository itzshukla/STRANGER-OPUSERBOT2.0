from ... import *
from SHUKLA.modules.clients.utils import *
from SHUKLA.modules.mongo.streams import *
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound
import logging

logger = logging.getLogger(__name__)

# End Stream (end)
@app.on_message(commandz(["end"]) & SUDOERS)
async def end_stream(client, message):
    chat_id = message.chat.id
    try:
        queue = await db.get_queue(chat_id)
        if queue:
            await db.remove_queue(chat_id)
            await call.leave_group_call(chat_id)
            await eor(message, "**⏹ Stream Stopped!**")
        else:
            await eor(message, "**❌ Nothing Playing!**")
    except Exception as e:
        logger.error(f"❌ Error in end_stream: {e}")
        await eor(message, f"**Error:** `{e}`")

# End Stream (cend)
@app.on_message(cdz(["cend"]) & SUDOERS)
async def close_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")
    try:
        queue = await db.get_queue(chat_id)
        if queue:
            await db.remove_queue(chat_id)
            await call.leave_group_call(chat_id)
            await eor(message, "**⏹ Stream Stopped!**")
        else:
            await eor(message, "**❌ Nothing Playing!**")
    except GroupCallNotFound:
        await eor(message, "**❌ I am Not in VC!**")
    except Exception as e:
        logger.error(f"❌ Error in cend: {e}")
        await eor(message, f"**Error:** `{e}`")