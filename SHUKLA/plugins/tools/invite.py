import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType, UserStatus
from pyrogram.types import Message
from pyrogram.errors.exceptions.flood_420 import FloodWait
from ... import app, SUDO_USER
from ... import *

@app.on_message(cdz(["addmore"])  & (filters.me | filters.user(SUDO_USER)))
async def invite(client: Client, message: Message):
    r = await message.reply_text("Processing . . .")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    await r.edit_text(f"inviting users from {chat.username}")
    async for member in client.get_chat_members(chat.id):
        user = member.user
        rj = [
            UserStatus.ONLINE,
            UserStatus.OFFLINE,
            UserStatus.RECENTLY,
            UserStatus.LAST_WEEK,
        ]
        if user.status in rj:
            try:
                await client.add_chat_members(tgchat.id, user.id)
                await r.delete()
            except FloodWait as e:
                return
            except Exception as e:
                pass
              


__NAME__ = "Iɴᴠɪᴛᴇ"
__MENU__ = """
 `.invitesall` - .invitesall @groupusername
 """
