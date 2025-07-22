from pyrogram import filters

from ... import app, eor, cdx, cdz, call
from ...modules.helpers.wrapper import sudo_users_only
from ...modules.mongo.streams import get_chat_id
from ...modules.utilities import queues
from ...modules.utilities.streams import run_stream, get_stream, get_result


# Handle query parsing
def extract_query(text):
    if "?si=" in text:
        return text.split(None, 1)[1].split("?si=")[0]
    return text.split(None, 1)[1]


# Common player function
async def play_file(chat_id, file, stream_type, aux):
    if not call.is_running(chat_id):
        stream = await run_stream(file, stream_type)
        await call.join_group_call(chat_id, stream)
        return await aux.edit("🎧 Playing!")

    if queues.is_empty(chat_id):
        stream = await run_stream(file, stream_type)
        await call.change_stream(chat_id, stream)
        return await aux.edit("🎧 Playing!")
    else:
        position = await queues.put(chat_id, file=file, type=stream_type)
        return await aux.edit(f"🎶 Queued at position {position}")


# Audio Player
@app.on_message(cdz(["ply", "play"]) & ~filters.private)
@sudo_users_only
async def audio_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**🔄 Processing...**")

    type = "Audio"
    audio = (
        message.reply_to_message.audio or message.reply_to_message.voice
        if message.reply_to_message
        else None
    )

    try:
        if audio:
            await aux.edit("📥 Downloading audio...")
            file = await client.download_media(message.reply_to_message)
        else:
            if len(message.command) < 2:
                return await aux.edit("**🥀 Provide a song name or link to play.**")
            query = extract_query(message.text)
            results = await get_result(query)
            file = await get_stream(results[0], type)

        await play_file(chat_id, file, type, aux)

    except Exception as e:
        print(f"Audio Play Error: {e}")
        return await aux.edit("❌ **Failed to process the request!**")


# Video Player
@app.on_message(cdz(["vply", "vplay"]) & ~filters.private)
@sudo_users_only
async def video_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**🔄 Processing...**")

    type = "Video"
    video = (
        message.reply_to_message.video or message.reply_to_message.document
        if message.reply_to_message
        else None
    )

    try:
        if video:
            await aux.edit("📥 Downloading video...")
            file = await client.download_media(message.reply_to_message)
        else:
            if len(message.command) < 2:
                return await aux.edit("**🥀 Provide a video name or link to play.**")
            query = extract_query(message.text)
            results = await get_result(query)
            file = await get_stream(results[0], type)

        await play_file(chat_id, file, type, aux)

    except Exception as e:
        print(f"Video Play Error: {e}")
        return await aux.edit("❌ **Failed to process the request!**")


# Audio Player (from anywhere)
@app.on_message(cdz(["cply", "cplay"]))
@sudo_users_only
async def audio_stream_from_anywhere(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No VC chat set. Use `/setvc` to define one.**")

    message.chat.id = chat_id
    await audio_stream(client, message)


# Video Player (from anywhere)
@app.on_message(cdz(["cvply", "cvplay"]))
@sudo_users_only
async def video_stream_from_anywhere(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No VC chat set. Use `/setvc` to define one.**")

    message.chat.id = chat_id
    await video_stream(client, message)
