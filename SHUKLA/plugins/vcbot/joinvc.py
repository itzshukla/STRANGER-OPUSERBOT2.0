from ... import *
from SHUKLA.modules.clients.func import *
from SHUKLA.modules.clients.utils import *
from pyrogram import Client, filters
from pytgcalls import StreamType
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall, TelegramServerError, GroupCallNotFound
import logging
import os

logger = logging.getLogger(__name__)

# Path to silent audio file
SILENCE_FILE = "SHUKLA/resource/audio/silence.mp3"

# Join Voice Chat (vcjoin)
@app.on_message(commandz(["vcjoin"]) & SUDOERS)
async def join_voice_chat(client, message):
    chat_id = message.chat.id
    m = await eor(message, "**🔄 Joining Voice Chat ...**")
    try:
        if not os.path.exists(SILENCE_FILE):
            logger.error(f"❌ Silent audio file not found: {SILENCE_FILE}")
            await eor(message, "**❌ Error: Silent audio file not found. Please contact the bot admin.**")
            return
        await call.join_group_call(
            chat_id,
            AudioPiped(SILENCE_FILE, HighQualityAudio()),
            stream_type=StreamType().pulse_stream
        )
        await eor(message, "**✅ Successfully Joined Voice Chat!**")
    except NoActiveGroupCall:
        await eor(message, "**❌ No Active Voice Chat Found!**")
    except AlreadyJoinedError:
        await eor(message, "**❌ Already in Voice Chat!**")
    except TelegramServerError:
        await eor(message, "**❌ Telegram Server Error!**")
    except Exception as e:
        logger.error(f"❌ Error in vcjoin: {e}")
        await eor(message, f"**Error:** `{e}`")

# Join Voice Chat (cjoin)
@app.on_message(cdz(["cjoin"]) & SUDOERS)
async def custom_join_voice_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 Please Set A Chat To Join Stream❗**")
    m = await eor(message, "**🔄 Joining Voice Chat ...**")
    try:
        if not os.path.exists(SILENCE_FILE):
            logger.error(f"❌ Silent audio file not found: {SILENCE_FILE}")
            await eor(message, "**❌ Error: Silent audio file not found. Please contact the bot admin.**")
            return
        await call.join_group_call(
            chat_id,
            AudioPiped(SILENCE_FILE, HighQualityAudio()),
            stream_type=StreamType().pulse_stream
        )
        await eor(message, "**✅ Successfully Joined Voice Chat!**")
    except NoActiveGroupCall:
        await eor(message, "**❌ No Active Voice Chat Found!**")
    except AlreadyJoinedError:
        await eor(message, "**❌ Already in Voice Chat!**")
    except TelegramServerError:
        await eor(message, "**❌ Telegram Server Error!**")
    except Exception as e:
        logger.error(f"Error in cjoin: {e}")
        await eor(message, f"**Error:** `{e}`")

# Leave Voice Chat (vcleave)
@app.on_message(commandz(["vcleave"]) & SUDOERS)
async def leave_voice_chat(client, message):
    chat_id = message.chat.id
    m = await eor(message, "**🔄 Leaving Voice Chat ...**")
    try:
        await call.leave_group_call(chat_id)
        await db.remove_queue(chat_id)
        await eor(message, "**✅ Successfully Left Voice Chat!**")
    except GroupCallNotFound:
        await eor(message, "**❌ No Active Voice Chat Found!**")
    except Exception as e:
        logger.error(f"❌ Error in vcleave: {e}")
        await eor(message, f"**Error:** `{e}`")

# Leave Voice Chat (cvcleave)
@app.on_message(cdz(["cvcleave"]) & SUDOERS)
async def custom_leave_voice_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 Please Set A Chat To Leave Stream❗**")
    m = await eor(message, "**🔄 Leaving Voice Chat ...**")
    try:
        await call.leave_group_call(chat_id)
        await db.remove_queue(chat_id)
        await eor(message, "**✅ Successfully Left Voice Chat!**")
    except GroupCallNotFound:
        await eor(message, "**❌ No Active Voice Chat Found!**")
    except Exception as e:
        logger.error(f"Error in cvcleave: {e}")
        await eor(message, f"**Error:** `{e}`")