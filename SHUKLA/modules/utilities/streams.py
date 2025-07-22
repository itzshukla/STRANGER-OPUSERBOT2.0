import asyncio, os, yt_dlp

from . import queues
from ..clients.clients import call
from ...console import USERBOT_PICTURE

from asyncio.queues import QueueEmpty
from pytgcalls.types import *
from pytgcalls.types.stream import *
from youtubesearchpython.__future__ import VideosSearch


async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


async def get_result(query: str):
    results = VideosSearch(query, limit=1)
    for result in (await results.next())["result"]:
        url = result["link"]
        try:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        except:
            thumbnail = USERBOT_PICTURE

    return url, thumbnail


async def get_stream(link, type):
    if type == "Audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
        }
    elif type == "Video":
        ydl_opts = {
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
        }

    x = yt_dlp.YoutubeDL(ydl_opts)
    info = x.extract_info(link, False)
    file = os.path.join("downloads", f"{info['id']}.{info['ext']}")
    if os.path.exists(file):
        return file
    await run_async(x.download, [link])
    return file


async def run_stream(file, type):
    if type == "Audio":
        audio_stream = AudioStream(
            file_path=file,
            audio_parameters=AudioParameters(
                bitrate=48000,
                channels=2,
            ),
            stream_type=StreamType().local_stream,
        )
        stream = Stream(audio_stream)

    elif type == "Video":
        audio_stream = AudioStream(
            file_path=file,
            audio_parameters=AudioParameters(
                bitrate=48000,
                channels=2,
            ),
            stream_type=StreamType().local_stream,
        )
        video_stream = VideoStream(
            file_path=file,
            video_parameters=VideoParameters(
                width=1280,
                height=720,
                frame_rate=30,
            ),
            stream_type=StreamType().local_stream,
        )
        stream = Stream(audio_stream, video_stream)

    return stream


async def close_stream(chat_id):
    try:
        await queues.clear(chat_id)
    except QueueEmpty:
        pass
    try:
        return await call.leave_group_call(chat_id)
    except:
        pass
