from pyrogram import filters
from ... import app, eor, cdx, cdz, call
from ...modules.mongo.streams import get_chat_id
from ...modules.helpers.wrapper import sudo_users_only


@app.on_message(cdx(["join", "joinvc"]) & ~filters.private)
@sudo_users_only
async def join_vc(client, message):
    chat_id = message.chat.id

    active_calls = call._call._calls  # INTERNAL: check active call dict
    if chat_id in active_calls:
        return await eor(message, "**✅ Already joined VC!**")

    try:
        await call.join_call(chat_id)
        await eor(message, "**🎧 Joined VC successfully!**")
    except Exception as e:
        print(f"Error: {e}")
        await eor(message, "**❌ Failed to join VC!**")


@app.on_message(cdz(["cjoin", "cjoinvc"]))
@sudo_users_only
async def join_vc_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)

    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")

    active_calls = call._call._calls
    if chat_id in active_calls:
        return await eor(message, "**✅ Already joined VC!**")

    try:
        await call.join_call(chat_id)
        await eor(message, "**🎧 Joined VC successfully!**")
    except Exception as e:
        print(f"Error: {e}")
        await eor(message, "**❌ Failed to join VC!**")
