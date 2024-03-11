from pyrogram import Client, filters
from gtts import gTTS
from ... import *
from ... import app, SUDO_USER

@app.on_message(
    filters.command(["tts"], ".") & (filters.me | filters.user(SUDO_USER))
)
def text_to_speech(client, message):
    text = message.text.split(' ', 1)[2]
    tts = gTTS(text=text, lang='hi')
    tts.save('sʜᴜᴋʟᴀ ᴀᴜᴅɪᴏ.mp3')
    client.send_audio(message.chat.id, 'sʜᴜᴋʟᴀ ᴀᴜᴅɪᴏ.mp3')
  

__NAME__ = "Tᴛs"
__MENU__ = """
`.tts` - **text to speech .**

"""
