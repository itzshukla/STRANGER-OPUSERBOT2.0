from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFoundError
from ... import app, eor, cdx, cdz, call
from ...modules.helpers.wrapper import sudo_users_only
from ...modules.mongo.streams import get_chat_id
from ...modules.utilities import queues
from ...modules.utilities.streams import run_stream

@app.on_message(cdx(["skp", "skip"]) & ~filters.private)
@sudo_users_only
async def skip_stream(client, message):
    chat_id = message.chat.id
    try:
        if not call.is_running(chat_id):
            return await eor(message, "**I am Not in VC!**")

        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await call.leave(chat_id)
            return await eor(message, "**Empty Queue, So\nLeaving VC!**")

        next_track = queues.get(chat_id)
        file = next_track["file"]
        type = next_track["type"]
        stream = await run_stream(file, type)
        await call.change_stream(chat_id, stream)
        return await eor(message, "**Stream Skipped!**")

    except GroupCallNotFoundError:
        return await eor(message, "**I am Not in VC!**")
    except Exception as e:
        print(f"Skip error: {e}")
        await eor(message, "**❌ Failed to skip track!**")


@app.on_message(cdz(["cskp", "cskip"]) & ~filters.private)
@sudo_users_only
async def skip_stream_custom(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")

    try:
        if not call.is_running(chat_id):
            return await eor(message, "**I am Not in VC!**")

        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await call.leave(chat_id)
            return await eor(message, "**Empty Queue, So\nLeaving VC!**")

        next_track = queues.get(chat_id)
        file = next_track["file"]
        type = next_track["type"]
        stream = await run_stream(file, type)
        await call.change_stream(chat_id, stream)
        return await eor(message, "**Stream Skipped!**")

    except GroupCallNotFoundError:
        return await eor(message, "**I am Not in VC!**")
    except Exception as e:
        print(f"Skip error: {e}")
        await eor(message, "**❌ Failed to skip track!**")
