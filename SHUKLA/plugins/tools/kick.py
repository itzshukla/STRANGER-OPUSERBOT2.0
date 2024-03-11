
from ... import app, SUDO_USER
from ... import *
from SHUKLA.modules.SHASHANK.data import GROUP
from pyrogram import Client, filters
from pyrogram.types import Message



@app.on_message(cdz(["join"])  & (filters.me | filters.user(SUDO_USER)))
async def join(xspam: Client, message: Message):
    alt = message.text.split(" ")
    if len(alt) == 1:
        return await message.reply_text("`Need a chat username or chat-id or invite link to join.`")
    try:
        await xspam.join_chat(alt[1])
        await message.reply_text(f"**Joined ✅**")
    except Exception as ex:
        await message.reply_text(f"**ERROR:** \n\n{str(ex)}")
  
         
@app.on_message(cdz(["kickme"])  & (filters.me | filters.user(SUDO_USER)))
async def leave(xspam: Client, message: Message):
    alt = message.text.split(" ")
    if len(alt) > 1:
        if alt[1] in GROUP:
            return
        try:
           await xspam.leave_chat(alt[1])
           await message.reply_text(f"**Left Successfully ✅**")
        except Exception as ex:
           await message.reply_text(f"**ERROR:** \n\n{str(ex)}")
    else:
        chat = message.chat.id
        ok = message.from_user.id
        if chat == ok:
            return await message.reply_text(f"⚡ ᴜsᴀɢᴇ:\n !leave <chat username or id> or !leave [type in Group for Direct leave]")
        elif chat in GROUP:
              return
        try:
           await xspam.leave_chat(chat)
           await message.reply_text(f"**Left Successfully ✅ **")
        except Exception as ex:
           await message.reply_text(f"**ERROR:** \n\n{str(ex)}")


__NAME__ = "Lᴇᴀᴠᴇ"
__MENU__ = """
`.join` **join group username **
`.kickme` **leave group **
"""
