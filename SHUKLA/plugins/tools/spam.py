from ... import app, SUDO_USER
from ... import *
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message


@app.on_message(filters.me & filters.command(["spam", "statspam", "slowspam"], "."))
async def spam(client: Client, message: Message):
    amount = int(message.command[1])
    text = " ".join(message.command[2:])
    spam_type = message.command[0]

    await message.delete()

    for msg in range(amount):
        if message.reply_to_message:
            sent = await message.reply_to_message.reply(text)
        else:
            sent = await client.send_message(message.chat.id, text)

        if spam_type == "statspam":
            await asyncio.sleep(0.1)
            await sent.delete()
        elif spam_type == "spam":
            await asyncio.sleep(0.1)
        elif spam_type == "slowspam":
            await asyncio.sleep(0.9)


@app.on_message(filters.me & filters.command(["fastspam"], "."))
async def fastspam(client: Client, message: Message):
    amount = int(message.command[1])
    text = " ".join(message.command[2:])

    await message.delete()

    coros = []
    for msg in range(amount):
        if message.reply_to_message:
            coros.append(message.reply_to_message.reply(text))
        else:
            coros.append(client.send_message(message.chat.id, text))
    await asyncio.wait(coros)
