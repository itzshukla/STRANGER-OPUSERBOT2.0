from ... import app, eor, cdx
from ...modules.mongo.streams import set_chat_id
from ...modules.helpers.wrapper import sudo_users_only
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid


@app.on_message(cdx(["cset", "schat", "setchat"]))
@sudo_users_only
async def set_stream_chat(client, message: Message):
    aux = await eor(message, "**Processing...**")
    user_id = message.from_user.id

    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        raw_input = message.text.split(None, 1)[1]
        try:
            if raw_input.startswith("@"):
                username = raw_input[1:]
                chat = await app.get_chat(username)
                chat_id = chat.id
            else:
                chat_id = int(raw_input)
        except (ValueError, PeerIdInvalid):
            return await aux.edit("**⚠️ Invalid Chat ID or Username!**")
        except Exception as e:
            print(f"Chat fetch error: {e}")
            return await aux.edit("**❌ Error fetching chat!**")

    if len(str(chat_id)) < 10:  # Better than fixed length == 14
        return await aux.edit("**⚠️ Invalid Chat ID Format!**")

    try:
        already_set = await set_chat_id(user_id, int(chat_id))
        if already_set:
            return await aux.edit("✅ **Stream chat already set!**")
        return await aux.edit("✅ **Stream chat saved successfully!**")
    except Exception as e:
        print(f"MongoDB Error: {e}")
        await aux.edit("**❌ Failed to set chat ID. Try again.**")
