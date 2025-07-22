import os
import asyncio
import yt_dlp

from . import queues
from ..clients.clients import call
from ...console import USERBOT_PICTURE

from asyncio.queues import QueueEmpty
from pytgcalls.types.stream import Stream
from pytgcalls.types.input_stream import (
    AudioStream,
    AudioParameters,
    VideoStream,
    VideoParameters,
)
from youtubesearchpython.__future__ import VideosSearch


async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


async def get_result(query: str):
    results = VideosSearch(query, limit=1)
    for result in (await results.next())["result"]:
        url = result["link"]
        thumbnail = result.get("thumbnails", [{}])[0].get("url", USERBOT_PICTURE).split("?")[0]
        return url, thumbnail
    return None, USERBOT_PICTURE


async def get_stream(link: str, type_: str) -> str:
    ydl_opts = {
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }

    if type_ == "Audio":
        ydl_opts["format"] = "bestaudio/best"
    elif type_ == "Video":
        ydl_opts["format"] = "(bestvideo[height<=720][width<=1280][ext=mp4])+(bestaudio[ext=m4a])"

    x = yt_dlp.YoutubeDL(ydl_opts)
    info = x.extract_info(link, download=False)
    file_path = os.path.join("downloads", f"{info['id']}.{info['ext']}")

    if not os.path.exists(file_path):
        await run_async(x.download, [link])

    return file_path


async def run_stream(file: str, type_: str) -> Stream:
    audio_stream = AudioStream(
        path=f"ffmpeg -i {file} -f s16le -ac 2 -ar 48000 pipe:1",
        parameters=AudioParameters(
            bitrate=48000,
            channels=2,
        ),
    )

    if type_ == "Audio":
        return Stream(audio_stream)

    elif type_ == "Video":
        video_stream = VideoStream(
            path=f"ffmpeg -i {file} -f rawvideo -r 30 -pix_fmt yuv420p -vf scale=1280:720 pipe:1",
            parameters=VideoParameters(
                width=1280,
                height=720,
                frame_rate=30,
            ),
        )
        return Stream(audio_stream, video_stream)


async def close_stream(chat_id: int):
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    try:
        await call.leave_group_call(chat_id)
    except Exception:
        pass
