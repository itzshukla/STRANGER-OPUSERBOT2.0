from ... import *
from SHUKLA.modules.clients.utils import *
from SHUKLA.modules.mongo.streams import *
from pyrogram import filters
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo
from pytgcalls.exceptions import NoActiveGroupCall, TelegramServerError, GroupCallNotFound
import logging

logger = logging.getLogger(__name__)

# Seek Stream (seek)
@app.on_message(commandz(["seek"]) & SUDOERS)
async def seek_stream(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await eor(message, "**🤖 Please provide a seek time (e.g., .seek 10)**")
    try:
        seconds = int(message.command[1])
        if seconds < 0:
            return await eor(message, "**🤖 Backward seeking is not supported! Use a positive number (e.g., .seek 10)**")
        queue = await db.get_queue(chat_id)
        if not queue:
            return await eor(message, "**❌ Nothing Playing!**")
        file = queue[0]["file"]
        stream_type = queue[0]["type"]
        song_name, duration = await get_media_info(file)
        # Use FFmpeg -ss parameter for seeking
        ffmpeg_params = f"-ss {seconds}"
        if stream_type == "Audio":
            stream = AudioPiped(file, HighQualityAudio(), additional_ffmpeg_parameters=ffmpeg_params)
        elif stream_type == "Video":
            stream = AudioVideoPiped(file, HighQualityAudio(), HighQualityVideo(), additional_ffmpeg_parameters=ffmpeg_params)
        await change_stream(client, chat_id, stream)
        queue[0]["played"] = seconds
        await db.set_queue(chat_id, queue)
        message_text = (
            f"**🥳 {stream_type} Streaming Started!**\n"
            f"**Song:** {song_name}\n"
            f"**Duration:** {format_duration(duration)}\n"
            f"**Seek:** Forward by {seconds} seconds"
        )
        await eor(message, message_text)
    except GroupCallNotFound:
        await eor(message, "**❌ I am Not in VC!**")
    except ValueError:
        await eor(message, "**🤖 Invalid seek time! Use a positive number (e.g., .seek 10)**")
    except Exception as e:
        logger.error(f"❌ Error in seek_stream: {e}")
        await eor(message, f"**Error:** `{e}`")

# Seek Stream (cseek)
@app.on_message(cdz(["cseek"]) & SUDOERS)
async def seek_stream_(client, message):
    if not message.from_user:
        return await eor(message, "**🤖 This command cannot be used by anonymous users!**")
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")
    if len(message.command) < 2:
        return await eor(message, "**🤖 Please provide a seek time (e.g., .cseek 10)**")
    try:
        seconds = int(message.command[1])
        if seconds < 0:
            return await eor(message, "**🤖 Backward seeking is not supported! Use a positive number (e.g., .cseek 10)**")
        queue = await db.get_queue(chat_id)
        if not queue:
            return await eor(message, "**❌ Nothing Playing!**")
        file = queue[0]["file"]
        stream_type = queue[0]["type"]
        song_name, duration = await get_media_info(file)
        # Use FFmpeg -ss parameter for seeking
        ffmpeg_params = f"-ss {seconds}"
        if stream_type == "Audio":
            stream = AudioPiped(file, HighQualityAudio(), additional_ffmpeg_parameters=ffmpeg_params)
        elif stream_type == "Video":
            stream = AudioVideoPiped(file, HighQualityAudio(), HighQualityVideo(), additional_ffmpeg_parameters=ffmpeg_params)
        await change_stream(client, chat_id, stream)
        queue[0]["played"] = seconds
        await db.set_queue(chat_id, queue)
        message_text = (
            f"**🥳 {stream_type} Streaming Started!**\n"
            f"**Song:** {song_name}\n"
            f"**Duration:** {format_duration(duration)}\n"
            f"**Seek:** Forward by {seconds} seconds"
        )
        await eor(message, message_text)
    except GroupCallNotFound:
        await eor(message, "**❌ I am Not in VC!**")
    except ValueError:
        await eor(message, "**🤖 Invalid seek time! Use a positive number (e.g., .cseek 10)**")
    except Exception as e:
        logger.error(f"❌ Error in cseek: {e}")
        await eor(message, f"**Error:** `{e}`")

# Speed Stream (speed)
@app.on_message(commandz(["speed"]) & SUDOERS)
async def speed_stream(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await eor(message, "**🤖 Please provide a speed value (e.g., .speed 1.5)**")
    try:
        speed = float(message.command[1])
        if not 0.5 <= speed <= 2.0:
            return await eor(message, "**🤖 Speed must be between 0.5 and 2.0 (e.g., .speed 1.5)**")
        queue = await db.get_queue(chat_id)
        if not queue:
            return await eor(message, "**❌ Nothing Playing!**")
        file = queue[0]["file"]
        stream_type = queue[0]["type"]
        song_name, duration = await get_media_info(file)
        await speedup_stream(chat_id, file, speed, queue)
        adjusted_duration = int(duration / speed) if isinstance(duration, int) else duration
        message_text = (
            f"**🥳 {stream_type} Streaming Started!**\n"
            f"**Song:** {song_name}\n"
            f"**Duration:** {format_duration(adjusted_duration)}\n"
            f"**Speed:** {speed}x"
        )
        await eor(message, message_text)
    except GroupCallNotFound:
        await eor(message, "**❌ I am Not in VC!**")
    except ValueError:
        await eor(message, "**🤖 Invalid speed value! Use a number between 0.5 and 2.0 (e.g., .speed 1.5)**")
    except Exception as e:
        logger.error(f"❌ Error in speed_stream: {e}")
        await eor(message, f"**Error:** `{e}`")

# Speed Stream (cspeed)
@app.on_message(cdz(["cspeed"]) & SUDOERS)
async def speed_stream_(client, message):
    if not message.from_user:
        return await eor(message, "**🤖 This command cannot be used by anonymous users!**")
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")
    if len(message.command) < 2:
        return await eor(message, "**🤖 Please provide a speed value (e.g., .cspeed 1.5)**")
    try:
        speed = float(message.command[1])
        if not 0.5 <= speed <= 2.0:
            return await eor(message, "**🤖 Speed must be between 0.5 and 2.0 (e.g., .cspeed 1.5)**")
        queue = await db.get_queue(chat_id)
        if not queue:
            return await eor(message, "**❌ Nothing Playing!**")
        file = queue[0]["file"]
        stream_type = queue[0]["type"]
        song_name, duration = await get_media_info(file)
        await speedup_stream(chat_id, file, speed, queue)
        adjusted_duration = int(duration / speed) if isinstance(duration, int) else duration
        message_text = (
            f"**🥳 {stream_type} Streaming Started!**\n"
            f"**Song:** {song_name}\n"
            f"**Duration:** {format_duration(adjusted_duration)}\n"
            f"**Speed:** {speed}x"
        )
        await eor(message, message_text)
    except GroupCallNotFound:
        await eor(message, "**❌ I am Not in VC!**")
    except ValueError:
        await eor(message, "**🤖 Invalid speed value! Use a number between 0.5 and 2.0 (e.g., .cspeed 1.5)**")
    except Exception as e:
        logger.error(f"❌ Error in cspeed: {e}")
        await eor(message, f"**Error:** `{e}`")

# Bassboost Stream (bassboost)
@app.on_message(commandz(["bassboost"]) & SUDOERS)
async def bassboost_stream(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await eor(message, "**🤖 Please provide a bass gain value (e.g., .bassboost 10)**")
    try:
        gain = float(message.command[1])
        if not -20 <= gain <= 20:
            return await eor(message, "**🤖 Bass gain must be between -20 and 20 dB (e.g., .bassboost 10)**")
        queue = await db.get_queue(chat_id)
        if not queue:
            return await eor(message, "**❌ Nothing Playing!**")
        file = queue[0]["file"]
        stream_type = queue[0]["type"]
        song_name, duration = await get_media_info(file)
        await bassboost_stream(chat_id, file, gain, queue)
        message_text = (
            f"**🥳 {stream_type} Streaming Started!**\n"
            f"**Song:** {song_name}\n"
            f"**Duration:** {format_duration(duration)}\n"
            f"**Bassboost:** {gain} dB"
        )
        await eor(message, message_text)
    except GroupCallNotFound:
        await eor(message, "**❌ I am Not in VC!**")
    except ValueError:
        await eor(message, "**🤖 Invalid bass gain value! Use a number between -20 and 20 (e.g., .bassboost 10)**")
    except Exception as e:
        logger.error(f"❌ Error in bassboost_stream: {e}")
        await eor(message, f"**Error:** `{e}`")

# Bassboost Stream (cbassboost)
@app.on_message(cdz(["cbassboost"]) & SUDOERS)
async def bassboost_stream_(client, message):
    if not message.from_user:
        return await eor(message, "**🤖 This command cannot be used by anonymous users!**")
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")
    if len(message.command) < 2:
        return await eor(message, "**🤖 Please provide a bass gain value (e.g., .cbassboost 10)**")
    try:
        gain = float(message.command[1])
        if not -20 <= gain <= 20:
            return await eor(message, "**🤖 Bass gain must be between -20 and 20 dB (e.g., .cbassboost 10)**")
        queue = await db.get_queue(chat_id)
        if not queue:
            return await eor(message, "**❌ Nothing Playing!**")
        file = queue[0]["file"]
        stream_type = queue[0]["type"]
        song_name, duration = await get_media_info(file)
        await bassboost_stream(chat_id, file, gain, queue)
        message_text = (
            f"**🥳 {stream_type} Streaming Started!**\n"
            f"**Song:** {song_name}\n"
            f"**Duration:** {format_duration(duration)}\n"
            f"**Bassboost:** {gain} dB"
        )
        await eor(message, message_text)
    except GroupCallNotFound:
        await eor(message, "**❌ I am Not in VC!**")
    except ValueError:
        await eor(message, "**🤖 Invalid bass gain value! Use a number between -20 and 20 (e.g., .cbassboost 10)**")
    except Exception as e:
        logger.error(f"❌ Error in cbassboost: {e}")
        await eor(message, f"**Error:** `{e}`")