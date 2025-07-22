from pyrogram import filters
from ... import app, eor, cdx, cdz, call
from ...modules.mongo.streams import get_chat_id
from ...modules.helpers.wrapper import sudo_users_only


@app.on_message(cdx(["pse", "pause"]) & ~filters.private)
@sudo_users_only
async def pause_stream(client, message):
    chat_id = message.chat.id
    if not call.is_running(chat_id):
        return await eor(message, "**❌ Nothing is currently streaming.**")
    try:
        await call.pause_stream(chat_id)
        await eor(message, "**⏸️ Stream paused.**")
    except Exception as e:
        print(f"[Pause Error] {e}")
        await eor(message, "**⚠️ Failed to pause stream.**")


@app.on_message(cdz(["cpse", "cpause"]))
@sudo_users_only
async def pause_stream_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No stream chat set. Use `/setvc` first.**")
    if not call.is_running(chat_id):
        return await eor(message, "**❌ Nothing is currently streaming.**")
    try:
        await call.pause_stream(chat_id)
        await eor(message, "**⏸️ Stream paused.**")
    except Exception as e:
        print(f"[Pause Error] {e}")
        await eor(message, "**⚠️ Failed to pause stream.**")
