import asyncio
import logging
import os
from ... import *
import motor.motor_asyncio
from typing import Union, List, Dict, Optional
from math import ceil
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
import yt_dlp
from youtubesearchpython import VideosSearch
import re

PREFIXES = Config.COMMAND_PREFIXES
HANDLERS = Config.COMMAND_HANDLERS

logger = logging.getLogger(__name__)

COOKIES_PATH = "cookies.txt"  # Path to cookies file

def commandx(commands: Union[str, List[str]]):
    return filters.command(commands, PREFIXES)

def commandz(commands: Union[str, List[str]]):
    return filters.command(commands, HANDLERS)

def get_youtube_id(url: str) -> str:
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else url

def format_duration(duration: Union[str, int]) -> str:
    """Convert duration (integer seconds or MM:SS string) to MM:SS minutes format."""
    if duration == "Unknown" or not duration:
        return "Unknown"
    try:
        if isinstance(duration, int):
            minutes = duration // 60
            secs = duration % 60
            return f"{minutes}:{secs:02d} minutes"
        parts = duration.split(":")
        if len(parts) == 2:
            minutes, secs = map(int, parts)
            return f"{minutes}:{secs:02d} minutes"
        return "Unknown"
    except (ValueError, TypeError):
        return "Unknown"

async def get_youtube_video(query: str):
    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio",
            "skip_download": True,
            "geturl": True,
            "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.debug(f"🔍 sᴇᴀʀᴄʜɪɴɢ ʏᴏᴜᴛᴜʙᴇ ғᴏʀ: {query}")
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            if "entries" not in result or not result["entries"]:
                logger.error(f"❌ ɴᴏ ʏᴏᴜᴛᴜʙᴇ ʀᴇsᴜʟᴛs ғᴏʀ ᴇᴜᴇʀʏ: {query}")
                return None
            video = result["entries"][0]
            logger.info(f"✅ ғᴏᴜɴᴅ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ: {video['webpage_url']}")
            return [video["webpage_url"], video["title"], video["duration"]]
    except Exception as e:
        logger.error(f"❌ ᴇʀʀᴏʀ ɪɴ ʏᴏᴜᴛᴜʙᴇ sᴇᴀʀᴄʜ: {e}")
        return None

async def audio_dl(vid_id: str):
    try:
        file_path = os.path.join("downloads", f"{vid_id}.mp3")
        temp_file_path = os.path.join("downloads", f"{vid_id}.mp3.mp3")
        if os.path.exists(file_path):
            logger.info(f"✅ ᴀᴜᴅɪᴏ ғɪʟᴇ ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs: {file_path}")
            return file_path
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join("downloads", f"{vid_id}.%(ext)s"),
            "quiet": False,
            "no_warnings": False,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "ffmpeg_location": "/usr/bin/ffmpeg",
            "keepvideo": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.debug(f"📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ: https://www.youtube.com/watch?v={vid_id}")
            ydl.download([f"https://www.youtube.com/watch?v={vid_id}"])
        if os.path.exists(temp_file_path):
            os.rename(temp_file_path, file_path)
            logger.info(f"✅ ʀᴇɴᴀᴍᴇᴅ {temp_file_path} ᴛᴏ {file_path}")
        if os.path.exists(file_path):
            logger.info(f"✅ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ᴀᴜᴅɪᴏ: {file_path}")
            return file_path
        logger.error(f"❌ ᴀᴜᴅɪᴏ ғɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ: {file_path}")
        return None
    except Exception as e:
        logger.error(f"❌ ᴇʀʀᴏʀ ɪɴ ᴀᴜᴅɪᴏ_ᴅʟ: {e}")
        return None

async def video_dl(vid_id: str):
    try:
        file_path = os.path.join("downloads", f"{vid_id}.mp4")
        if os.path.exists(file_path):
            logger.info(f"✅ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs: {file_path}")
            return file_path
        ydl_opts = {
            "format": "bestvideo[height<=720][width<=1280]+bestaudio/best",
            "outtmpl": file_path,
            "quiet": False,
            "no_warnings": False,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
            "merge_output_format": "mp4",
            "ffmpeg_location": "/usr/bin/ffmpeg",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.debug(f"📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ: https://www.youtube.com/watch?v={vid_id}")
            ydl.download([f"https://www.youtube.com/watch?v={vid_id}"])
        if os.path.exists(file_path):
            logger.info(f"✅ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ᴠɪᴅᴇᴏ: {file_path}")
            return file_path
        logger.error(f"❌ ᴠɪᴅᴇᴏ ғɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ: {file_path}")
        return None
    except Exception as e:
        logger.error(f"❌ ᴇʀʀᴏʀ ɪɴ ᴠɪᴅᴇᴏ_ᴅʟ: {e}")
        return None

async def get_media_info(file: str, query: str = None, videoid: Union[bool, str] = None) -> tuple:
    try:
        if query and videoid:
            # For YouTube searches
            link = f"https://www.youtube.com/watch?v={videoid}"
            results = VideosSearch(link, limit=1)
            result = (await results.next())["result"][0]
            song_name = result["title"]
            duration = result["duration"] if result["duration"] != "None" else "Unknown"
        else:
            # For direct file uploads
            song_name = query if query else os.path.basename(file).split(".")[0]
            duration = "Unknown"  # Fallback for direct uploads
        return song_name, duration
    except Exception as e:
        logger.error(f"Error getting media info: {e}")
        return os.path.basename(file).split(".")[0], "Unknown"

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_DATABASE)
        self.db = self.client["music_bot"]
        self.queues_collection = self.db["queues"]

    async def get_queue(self, chat_id: int):
        try:
            queue_doc = await self.queues_collection.find_one({"chat_id": chat_id})
            return queue_doc.get("queue") if queue_doc else None
        except Exception as e:
            logger.error(f"Error in get_queue: {e}")
            return None

    async def set_queue(self, chat_id: int, queue: list):
        try:
            await self.queues_collection.update_one(
                {"chat_id": chat_id},
                {"$set": {"queue": queue}},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error in set_queue: {e}")

    async def remove_queue(self, chat_id: int):
        try:
            await self.queues_collection.delete_one({"chat_id": chat_id})
        except Exception as e:
            logger.error(f"Error in remove_queue: {e}")

    async def put_que(self, chat_id: int, file: str, type: str):
        try:
            put = {
                "chat_id": chat_id,
                "file": file,
                "type": type,
            }
            queue_doc = await self.queues_collection.find_one({"chat_id": chat_id})
            if not queue_doc:
                queue = [put]
                await self.queues_collection.insert_one({"chat_id": chat_id, "queue": queue})
                return 1
            else:
                queue = queue_doc.get("queue", [])
                queue.append(put)
                await self.queues_collection.update_one(
                    {"chat_id": chat_id},
                    {"$set": {"queue": queue}},
                    upsert=True
                )
                return len(queue)
        except Exception as e:
            logger.error(f"Error in put_que: {e}")
            return None

db = Database()