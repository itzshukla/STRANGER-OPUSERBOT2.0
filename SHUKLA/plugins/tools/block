from pyrogram import Client, filters
from pyrogram.types import Message
from ... import app, SUDO_USER
from ... import *

blacklist = set()

# Command to add blacklist word
@app.on_message(cdz(["blockword"])  & (filters.me | filters.user(SUDO_USER))
)
def add_blackword(client, message: Message):
    if len(message.command) > 1:
        word = message.command[1].lower()
        blacklist.add(word)
        message.reply(f"'{word}' has been added to the blacklist.")
    else:
        message.reply("Please provide a word to add to the blacklist.")

# Command to remove blacklist word
@app.on_message(cdz(["unblockword"])  & (filters.me | filters.user(SUDO_USER))
)
def remove_blackword(client, message: Message):
    if len(message.command) > 1:
        word = message.command[1].lower()
        if word in blacklist:
            blacklist.remove(word)
            message.reply(f"'{word}' has been removed from the blacklist.")
        else:
            message.reply(f"'{word}' is not in the blacklist.")
    else:
        message.reply("Please provide a word to remove from the blacklist.")

# Filter messages and check for blacklist words
@app.on_message(filters.text)
def check_blacklist(client, message: Message):
    for word in message.text.lower().split():
        if word in blacklist:
            message.delete()
            message.reply("This message contains a blacklisted word and has been deleted.")
            break
