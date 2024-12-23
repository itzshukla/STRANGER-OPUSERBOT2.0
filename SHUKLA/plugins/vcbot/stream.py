import yt_dlp as ytdl
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
#from pytgcalls.types import AudioPiped, VideoPiped
from pytgcalls.exceptions import GroupCallNotFound
from ...modules.mongo.streams import *
from ...modules.utilities import queues
from pytgcalls.types import GroupCall

from ... import bot, app, call

# Define the get_result function with cookies path
async def get_result(query, cookies_path):
    try:
        # Set up yt-dlp options with cookies
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'cookies': cookies_path,  # Use the cookies file path
            'quiet': True,
        }
        # Search and fetch info using yt-dlp
        with ytdl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            results = info.get('entries', [])
            if results:
                return results[0]['url']  # Return the URL of the first result
            else:
                return None
    except Exception as e:
        print(f"Error in get_result: {e}")
        return None

# Audio streaming handler
@app.on_message(filters.command(["ply", "play"]) & ~filters.private)
async def audio_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**Processing...**")
    cookies_path = 'cookies.txt'  # Path to your cookies.txt file

    try:
        # Check if the message is a reply to audio/voice
        audio = (
            message.reply_to_message.audio
            or message.reply_to_message.voice
            if message.reply_to_message
            else None
        )
        if audio:
            await aux.edit("Downloading...")
            file = await client.download_media(message.reply_to_message)
        else:
            # Handle query-based playback
            if len(message.command) < 2:
                return await aux.edit("**🥀 Provide a query to play music!**")
            query = message.text.split(None, 1)[1]
            file = await get_result(query, cookies_path)
            if not file:
                return await aux.edit("**🥀 No results found!**")
        
        # Stream the audio
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = AudioPiped(file)
                await call.join_group_call(chat_id, stream)
                await aux.edit("**Playing!**")
            elif a.status in ["playing", "paused"]:
                position = await queues.put(chat_id, file=file, type="Audio")
                await aux.edit(f"Queued at position {position}")
        except GroupCallNotFound:
            stream = AudioPiped(file)
            await call.join_group_call(chat_id, stream)
            await aux.edit("**Playing!**")
    except Exception as e:
        print(f"Error: {e}")
        await aux.edit("**Please try again!**")

# Video streaming handler
@app.on_message(filters.command(["vply", "vplay"]) & ~filters.private)
async def video_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**Processing...**")
    cookies_path = 'cookies.txt'  # Path to your cookies.txt file

    try:
        # Check if the message is a reply to video/document
        video = (
            message.reply_to_message.video
            or message.reply_to_message.document
            if message.reply_to_message
            else None
        )
        if video:
            await aux.edit("Downloading...")
            file = await client.download_media(message.reply_to_message)
        else:
            # Handle query-based playback
            if len(message.command) < 2:
                return await aux.edit("**🥀 Provide a query to play video!**")
            query = message.text.split(None, 1)[1]
            file = await get_result(query, cookies_path)
            if not file:
                return await aux.edit("**🥀 No results found!**")
        
        # Stream the video
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = VideoPiped(file)
                await call.join_group_call(chat_id, stream)
                await aux.edit("**Playing!**")
            elif a.status in ["playing", "paused"]:
                position = await queues.put(chat_id, file=file, type="Video")
                await aux.edit(f"Queued at position {position}")
        except GroupCallNotFound:
            stream = VideoPiped(file)
            await call.join_group_call(chat_id, stream)
            await aux.edit("**Playing!**")
    except Exception as e:
        print(f"Error: {e}")
        await aux.edit("**Please try again!**")
