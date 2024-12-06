from asyncio.queues import QueueEmpty
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound
from ... import *
from ...modules.mongo.streams import *
from ...modules.utilities import queues

# Audio Player

@app.on_message(cdz(["ply", "play"]) & ~filters.private)
@sudo_users_only
async def audio_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**Processing ...**")
    audio = (
        (
            message.reply_to_message.audio
            or message.reply_to_message.voice
        )
        if message.reply_to_message
        else None
    )
    type = "Audio"
    try:
        if audio:
            await aux.edit("Downloading ...")
            file = await client.download_media(
                message.reply_to_message
            )
        else:
            if len(message.command) < 2:
                return await aux.edit(
                    "**🥀 ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ\nᴘʟᴀʏ ᴍᴜsɪᴄ ᴏʀ ᴠɪᴅᴇᴏ❗...**"
                )
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            
            # Use yt-dlp to get the video stream link with cookies
            ydl_opts = {
                'cookiefile': 'cookies.txt',  # Provide the path to your cookie file here
                'quiet': True,
                'format': 'bestaudio/best',
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(query, download=False)
                if 'entries' in result:
                    # Take the first video in the playlist
                    link = result['entries'][0]['url']
                else:
                    # If it's a single video
                    link = result['url']
            
            file = await get_stream(link, type)

        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = await run_stream(file, type)
                await call.change_stream(chat_id, stream)
                await aux.edit("Playing!")
            elif (a.status == "playing"
                or a.status == "paused"
            ):
                position = await queues.put(
                    chat_id, file=file, type=type
                )
                await aux.edit(f"Queued At {position}")
        except GroupCallNotFound:
            stream = await run_stream(file, type)
            await call.join_group_call(chat_id, stream)
            await aux.edit("Playing!")
    except Exception as e:
       print(f"Error: {e}")
       return await aux.edit("**Please Try Again !**")
    except:
        return
