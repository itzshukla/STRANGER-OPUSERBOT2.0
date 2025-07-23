from ... import *
from SHUKLA.modules.clients.utils import *
from pyrogram import filters
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.exceptions import GroupCallNotFound
import logging

logger = logging.getLogger(__name__)

# Skip Stream (skip)
@app.on_message(commandz(["skip"]) & SUDOERS)
async def skip_stream(client, message):
    chat_id = message.chat.id
    try:
        queue = await db.get_queue(chat_id)
        if queue:
            queue.pop(0)
            if not queue:
                await call.leave_group_call(chat_id)
                await db.remove_queue(chat_id)
                await eor(message, "**⏹ Empty Queue, Stream Stopped!**")
            else:
                file = queue[0]["file"]
                stream_type = queue[0]["type"]
                song_name, duration = await get_media_info(file)
                if stream_type == "Audio":
                    stream = AudioPiped(file, HighQualityAudio())
                elif stream_type == "Video":
                    stream = AudioVideoPiped(file, HighQualityAudio(), HighQualityVideo())
                await db.set_queue(chat_id, queue)
                await call.change_stream(chat_id, stream)
                await eor(message, f"**⏭ Skipped to Next Stream!**\n**Song:** {song_name}\n**Duration:** {duration}")
        else:
            await eor(message, "**❌ Nothing Playing!**")
    except Exception as e:
        logger.error(f"❌ Error in skip_stream: {e}")
        await eor(message, f"**Error:** `{e}`")

# Skip Stream (cskip)
@app.on_message(cdz(["cskp", "cskip"]) & SUDOERS & ~filters.private)
async def skip_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")
    try:
        queue = await db.get_queue(chat_id)
        if queue:
            queue.pop(0)
            if not queue:
                await call.leave_group_call(chat_id)
                await db.remove_queue(chat_id)
                await eor(message, "**⏹ Empty Queue, Stream Stopped!**")
            else:
                file = queue[0]["file"]
                stream_type = queue[0]["type"]
                song_name, duration = await get_media_info(file)
                if stream_type == "Audio":
                    stream = AudioPiped(file, HighQualityAudio())
                elif stream_type == "Video":
                    stream = AudioVideoPiped(file, HighQualityAudio(), HighQualityVideo())
                await db.set_queue(chat_id, queue)
                await call.change_stream(chat_id, stream)
                await eor(message, f"**⏭ Skipped to Next Stream!**\n**Song:** {song_name}\n**Duration:** {duration}")
        else:
            await eor(message, "**❌ Nothing Playing!**")
    except Exception as e:
        logger.error(f"❌ Error in cskip: {e}")
        await eor(message, f"**Error:** `{e}`")