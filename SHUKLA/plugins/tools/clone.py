import os
from pyrogram import *
from pyrogram.types import *
from ... import app, SUDO_USER
from ... import *
from SHUKLA.modules.SHASHANK.basic import edit_or_reply, get_text, get_user


OWNER = os.environ.get("OWNER", None)
BIO = os.environ.get("BIO", "ɪ ᴀᴍ ᴘᴀʀᴛ ᴏғ sᴛʀᴀɴɢᴇʀ ᴛᴇᴀᴍ ♡ ᴊᴏɪɴ ɴᴏᴡ @SHIVANSH474")


@app.on_message(cdz(["clone"])  & (filters.me | filters.user(SUDO_USER)))
async def clone(client: Client, message: Message):
    text = get_text(message)
    op = await message.edit_text("`Cloning`")
    userk = get_user(message, text)[0]
    user_ = await client.get_users(userk)
    if not user_:
        await op.edit("`Whom i should clone:(`")
        return

    get_bio = await client.get_chat(user_.id)
    f_name = user_.first_name
    c_bio = get_bio.bio
    pic = user_.photo.big_file_id
    poto = await client.download_media(pic)

    await client.set_profile_photo(photo=poto)
    await client.update_profile(
        first_name=f_name,
        bio=c_bio,
    )
    await message.edit(f"**From now I'm** __{f_name}__")


@app.on_message(cdz(["unclone"])  & (filters.me | filters.user(SUDO_USER)))
async def revert(client: Client, message: Message):
    await message.edit("`Reverting`")
    r_bio = BIO

    # Get ur Name back
    await client.update_profile(
        first_name=OWNER,
        bio=r_bio,
    )
    # Delte first photo to get ur identify
    photos = [p async for p in client.get_chat_photos("me")]
    await client.delete_profile_photos(photos[0].file_id)
    await message.edit("`I am back!`")


__NAME__ = " Cʟᴏɴᴇ "
__MENU__ = """
`.clone` - **reply_message for clone I'd**
`.unclone` - **reply_message to cloner to get back**
"""
