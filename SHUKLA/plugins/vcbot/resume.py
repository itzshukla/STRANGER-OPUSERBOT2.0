from pyrogram import filters
from ... import app, eor, cdx, cdz, call
from ...modules.helpers.wrapper import sudo_users_only
from ...modules.mongo.streams import get_chat_id


@app.on_message(cdx(["rsm", "resume"]) & ~filters.private)
@sudo_users_only
async def resume_stream(client, message):
    chat_id = message.chat.id
    if not call.is_running(chat_id):
        return await eor(message, "**❌ Nothing is currently streaming.**")
    try:
        await call.resume_stream(chat_id)
        await eor(message, "**▶️ Stream resumed.**")
    except Exception as e:
        print(f"[Resume Error] {e}")
        await eor(message, "**⚠️ Failed to resume stream.**")


@app.on_message(cdz(["crsm", "cresume"]))
@sudo_users_only
async def resume_stream_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No stream chat set. Use `/setvc` first.**")
    if not call.is_running(chat_id):
        return await eor(message, "**❌ Nothing is currently streaming.**")
    try:
        await call.resume_stream(chat_id)
        await eor(message, "**▶️ Stream resumed.**")
    except Exception as e:
        print(f"[Resume Error] {e}")
        await eor(message, "**⚠️ Failed to resume stream.**")
