from ... import call, app
from typing import Union
from SHUKLA.modules.clients.vars import Config
from SHUKLA.modules.clients.utils import *
from pyrogram.types import Message
from pytgcalls.types import Update
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall, TelegramServerError
import logging

logger = logging.getLogger(__name__)

async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    msg = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await msg(*args, **kwargs)

eor = edit_or_reply

async def put_que(chat_id: int, file: str, stream_type: str) -> int:
    put = {
        "chat_id": chat_id,
        "file": file,
        "type": stream_type,
    }
    try:
        check = await db.get_queue(chat_id)
        if not check:
            queue = [put]
            await db.set_queue(chat_id, queue)
            return 1
        else:
            queue = check
            queue.append(put)
            await db.set_queue(chat_id, queue)
            return len(queue)
    except Exception as e:
        logger.error(f"❌ Error in put_que: {e}")
        return None

async def run_stream(file: str, stream_type: str):
    try:
        if stream_type == "Audio":
            return AudioPiped(file, HighQualityAudio())
        elif stream_type == "Video":
            return AudioVideoPiped(file, HighQualityAudio(), HighQualityVideo())
        else:
            raise ValueError(f"Invalid stream type: {stream_type}")
    except Exception as e:
        logger.error(f"❌ Error in run_stream: {e}")
        raise

async def join_vc(chat_id: int, message: Message) -> bool:
    try:
        queue = await db.get_queue(chat_id)
        if not queue:
            await eor(message, "**❌ No Active Queue to Join!**")
            return False
        file = queue[0]["file"]
        stream_type = queue[0]["type"]
        if stream_type == "Audio":
            stream = AudioPiped(file, HighQualityAudio())
        elif stream_type == "Video":
            stream = AudioVideoPiped(file, HighQualityAudio(), HighQualityVideo())
        else:
            await eor(message, "**❌ Invalid Stream Type in Queue!**")
            return False
        await call.join_group_call(
            chat_id,
            stream,
            stream_type=StreamType().pulse_stream
        )
        await eor(message, f"**✅ Joined Voice Chat in {chat_id}!**")
        return True
    except NoActiveGroupCall:
        await eor(message, "**❌ No Active Voice Chat!**")
        return False
    except AlreadyJoinedError:
        await eor(message, "**❌ Already in Voice Chat!**")
        return False
    except TelegramServerError:
        await eor(message, "**❌ Telegram Server Error!**")
        return False
    except Exception as e:
        logger.error(f"❌ Error in join_vc: {e}")
        await eor(message, f"**Error:** `{e}`")
        return False

@call.on_kicked()
async def kicked_handler(_, chat_id: int):
    try:
        check = await db.get_queue(chat_id)
        if check:
            await db.remove_queue(chat_id)
            logger.info(f"✅ Removed queue for chat {chat_id} due to being kicked")
    except Exception as e:
        logger.error(f"❌ Error in kicked_handler: {e}")

@call.on_closed_voice_chat()
async def closed_voice_chat_handler(_, chat_id: int):
    try:
        check = await db.get_queue(chat_id)
        if check:
            await db.remove_queue(chat_id)
            logger.info(f"✅ Removed queue for chat {chat_id} due to closed voice chat")
    except Exception as e:
        logger.error(f"❌ Error in closed_voice_chat_handler: {e}")

@call.on_left()
async def left_handler(_, chat_id: int):
    try:
        check = await db.get_queue(chat_id)
        if check:
            await db.remove_queue(chat_id)
            logger.info(f"✅ Removed queue for chat {chat_id} due to leaving")
    except Exception as e:
        logger.error(f"❌ Error in left_handler: {e}")

@call.on_stream_end()
async def stream_end_handler(_, update: Update):
    chat_id = update.chat_id
    try:
        check = await db.get_queue(chat_id)
        if check:
            queue = check
            queue.pop(0)
            if len(queue) == 0:
                await db.remove_queue(chat_id)
                await call.leave_group_call(chat_id)
                await app.send_message(chat_id, "**⏹ Empty Queue, Stream Stopped!**")
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
                message_text = (
                    f"**🥳 {stream_type} Streaming Started!**\n"
                    f"**Song:** {song_name}\n"
                    f"**Duration:** {format_duration(duration)}"
                )
                await app.send_message(chat_id, message_text)
                logger.info(f"✅ Switched to next stream in queue for {chat_id}")
    except Exception as e:
        logger.error(f"❌ Error in stream_end_handler: {e}")
        await app.send_message(chat_id, f"**Error:** `{e}`")