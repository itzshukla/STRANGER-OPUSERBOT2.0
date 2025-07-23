from ... import *
from SHUKLA.modules.clients.func import *
from SHUKLA.modules.clients.utils import *
from pyrogram import Client, filters
from pytgcalls import StreamType
from SHUKLA.modules.mongo.streams import *
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall, TelegramServerError, GroupCallNotFound
import logging
import re

logger = logging.getLogger(__name__)

# Audio Stream (play)
@app.on_message(commandz(["ply", "play"]) & SUDOERS)
async def audio_stream(client, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    audio = (
        (replied.audio or replied.voice or replied.video or replied.document)
        if replied else None
    )
    query = message.text.split(None, 1)[1].split("?si")[0].strip() if len(message.command) > 1 else None
    m = await eor(message, "**🔄 Processing ...**")
    try:
        if audio:
            await m.edit("**📥 Downloading ...**")
            file = await replied.download()
            song_name, duration = await get_media_info(file, query)
        else:
            if not query:
                return await eor(message, "**🤖 Give Some Query ...**")
            await m.edit("**🔍 Searching ...**")
            search = await get_youtube_video(query)
            if not search:
                return await eor(message, "**❌ No Results Found!**")
            vid_id = get_youtube_id(search[0])
            file = await audio_dl(vid_id)
            if not file:
                return await eor(message, "**❌ Failed to Download Audio!**")
            song_name, duration = search[1], search[2]
        await m.edit("**🔄 Processing ...**")
        queue = await db.get_queue(chat_id)
        if not queue:
            try:
                await call.join_group_call(
                    chat_id,
                    AudioPiped(file, HighQualityAudio()),
                    stream_type=StreamType().pulse_stream
                )
                await put_que(chat_id, file, "Audio")
                await eor(message, f"**🥳 Audio Streaming Started!**\n**Song:** {song_name}\n**Duration:** {duration}")
            except NoActiveGroupCall:
                await eor(message, "**❌ No Active Voice Chat!**")
            except AlreadyJoinedError:
                await eor(message, "**❌ Already in Voice Chat!**")
            except TelegramServerError:
                await eor(message, "**❌ Telegram Server Error!**")
        else:
            pos = await put_que(chat_id, file, "Audio")
            await eor(message, f"**😋 Added to Queue #{pos}**\n**Song:** {song_name}\n**Duration:** {duration}")
    except Exception as e:
        logger.error(f"❌ Error in audio_stream: {e}")
        await eor(message, f"**Error:** `{e}`")

# Video Stream (vplay)
@app.on_message(commandz(["vplay"]) & SUDOERS)
async def video_stream(client, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    video = (
        (replied.audio or replied.voice or replied.video or replied.document)
        if replied else None
    )
    query = message.text.split(None, 1)[1].split("?si")[0].strip() if len(message.command) > 1 else None
    m = await eor(message, "**🔄 Processing ...**")
    try:
        if video:
            await m.edit("**📥 Downloading ...**")
            file = await replied.download()
            song_name, duration = await get_media_info(file, query)
        else:
            if not query:
                return await eor(message, "**🤖 Give Some Query ...**")
            await m.edit("**🔍 Searching ...**")
            search = await get_youtube_video(query)
            if not search:
                return await eor(message, "**❌ No Results Found!**")
            vid_id = get_youtube_id(search[0])
            file = await video_dl(vid_id)
            if not file:
                return await eor(message, "**❌ Failed to Download Video!**")
            song_name, duration = search[1], search[2]
        await m.edit("**🔄 Processing ...**")
        queue = await db.get_queue(chat_id)
        if not queue:
            try:
                await call.join_group_call(
                    chat_id,
                    AudioVideoPiped(file, HighQualityAudio(), HighQualityVideo()),
                    stream_type=StreamType().pulse_stream
                )
                await put_que(chat_id, file, "Video")
                await eor(message, f"**🥳 Video Streaming Started!**\n**Song:** {song_name}\n**Duration:** {duration}")
            except NoActiveGroupCall:
                await eor(message, "**❌ No Active Voice Chat!**")
            except AlreadyJoinedError:
                await eor(message, "**❌ Already in Voice Chat!**")
            except TelegramServerError:
                await eor(message, "**❌ Telegram Server Error!**")
        else:
            pos = await put_que(chat_id, file, "Video")
            await eor(message, f"**😋 Added to Queue #{pos}**\n**Song:** {song_name}\n**Duration:** {duration}")
    except Exception as e:
        logger.error(f"❌ Error in video_stream: {e}")
        await eor(message, f"**Error:** `{e}`")

# Audio Stream (cplay)
@app.on_message(cdz(["cply", "cplay"]) & SUDOERS)
async def audio_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 Please Set A Chat To Start Stream❗**")
    aux = await eor(message, "**🔄 Processing ...**")
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message else None
    )
    query = message.text.split(None, 1)[1].split("?si")[0] if len(message.command) > 1 else None
    type = "Audio"
    try:
        if audio:
            await aux.edit("**📥 Downloading ...**")
            file = await client.download_media(message.reply_to_message)
            song_name, duration = await get_media_info(file, query)
        else:
            if not query:
                return await aux.edit("**🥀 Give Some Query To Play Music Or Video❗**")
            search = await get_youtube_video(query)
            if not search:
                return await aux.edit("**❌ No Results Found!**")
            file = await audio_dl(get_youtube_id(search[0]))
            if not file:
                return await aux.edit("**❌ Failed to Download Audio!**")
            song_name, duration = search[1], search[2]
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = await run_stream(file, type)
                await call.change_stream(chat_id, stream)
                await aux.edit(f"**🥳 Audio Streaming Started!**\n**Song:** {song_name}\n**Duration:** {duration}")
            elif a.status in ["playing", "paused"]:
                position = await queues.put(chat_id, file=file, type=type)
                await aux.edit(f"**😋 Added to Queue #{position}**\n**Song:** {song_name}\n**Duration:** {duration}")
        except GroupCallNotFound:
            stream = await run_stream(file, type)
            await call.join_group_call(chat_id, stream)
            await aux.edit(f"**🥳 Audio Streaming Started!**\n**Song:** {song_name}\n**Duration:** {duration}")
    except Exception as e:
        logger.error(f"Error in cplay: {e}")
        await aux.edit("**Please Try Again!**")

# Video Stream (cvplay)
@app.on_message(cdz(["cvply", "cvplay"]) & SUDOERS)
async def video_stream_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 Please Set A Chat To Start Stream❗**")
    aux = await eor(message, "**🔄 Processing ...**")
    video = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message else None
    )
    query = message.text.split(None, 1)[1].split("?si")[0] if len(message.command) > 1 else None
    type = "Video"
    try:
        if video:
            await aux.edit("**📥 Downloading ...**")
            file = await client.download_media(message.reply_to_message)
            song_name, duration = await get_media_info(file, query)
        else:
            if not query:
                return await aux.edit("**🥀 Give Some Query To Play Music Or Video❗**")
            search = await get_youtube_video(query)
            if not search:
                return await aux.edit("**❌ No Results Found!**")
            file = await video_dl(get_youtube_id(search[0]))
            if not file:
                return await aux.edit("**❌ Failed to Download Video!**")
            song_name, duration = search[1], search[2]
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = await run_stream(file, type)
                await call.change_stream(chat_id, stream)
                await aux.edit(f"**🥳 Video Streaming Started!**\n**Song:** {song_name}\n**Duration:** {duration}")
            elif a.status in ["playing", "paused"]:
                position = await queues.put(chat_id, file=file, type=type)
                await aux.edit(f"**😋 Added to Queue #{position}**\n**Song:** {song_name}\n**Duration:** {duration}")
        except GroupCallNotFound:
            stream = await run_stream(file, type)
            await call.join_group_call(chat_id, stream)
            await aux.edit(f"**🥳 Video Streaming Started!**\n**Song:** {song_name}\n**Duration:** {duration}")
    except Exception as e:
        logger.error(f"Error in cvplay: {e}")
        await aux.edit("**Please Try Again!**")