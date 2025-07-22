from asyncio.queues import QueueEmpty
from pyrogram import filters

from ... import app, eor, cdx, cdz, call
from ...modules.helpers.wrapper import sudo_users_only
from ...modules.mongo.streams import get_chat_id
from ...modules.utilities import queues


# Stop stream (in group)
@app.on_message(cdx(["stp"]) & ~filters.private)
@sudo_users_only
async def stop_stream(client, message):
    chat_id = message.chat.id
    if not call.is_running(chat_id):
        return await eor(message, "**🤷 Nothing is currently streaming.**")
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await call.change_stream(chat_id)
    await eor(message, "**⏹️ Stream stopped.**")


# Stop stream (from anywhere)
@app.on_message(cdz(["cstp"]))
@sudo_users_only
async def stop_stream_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No VC chat set. Use `/setvc` first.**")
    if not call.is_running(chat_id):
        return await eor(message, "**🤷 Nothing is currently streaming.**")
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await call.change_stream(chat_id)
    await eor(message, "**⏹️ Stream stopped.**")


# End stream (leave VC)
@app.on_message(cdx(["end"]) & ~filters.private)
@sudo_users_only
async def close_stream(client, message):
    chat_id = message.chat.id
    if not call.is_running(chat_id):
        return await eor(message, "**🤷 I’m not in VC currently.**")
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await call.leave_group_call(chat_id)
    await eor(message, "**✅ Left the VC. Stream ended.**")


# End stream from anywhere
@app.on_message(cdz(["cend"]))
@sudo_users_only
async def close_stream_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No VC chat set. Use `/setvc` first.**")
    if not call.is_running(chat_id):
        return await eor(message, "**🤷 I’m not in VC currently.**")
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await call.leave_group_call(chat_id)
    await eor(message, "**✅ Left the VC. Stream ended.**")
