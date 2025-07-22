from asyncio.queues import QueueEmpty
from pyrogram import filters
from ... import app, eor, cdx, cdz, call
from ...modules.mongo.streams import get_chat_id
from ...modules.utilities import queues
from ...modules.helpers.wrapper import sudo_users_only


@app.on_message(cdx(["lve", "leave", "leavevc"]) & ~filters.private)
@sudo_users_only
async def leave_vc(client, message):
    chat_id = message.chat.id
    if not call.is_running(chat_id):
        return await eor(message, "**❌ I am not in VC!**")
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await call.leave_call(chat_id)
    await eor(message, "**✅ Left VC successfully!**")


@app.on_message(cdz(["clve", "cleave", "cleavevc"]))
@sudo_users_only
async def leave_vc_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")

    if not call.is_running(chat_id):
        return await eor(message, "**❌ I am not in VC!**")

    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await call.leave_call(chat_id)
    await eor(message, "**✅ Left VC successfully!**")
