import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp

# Telegram Login Details
API_ID = 6301598  # Apna API ID yahan daalein
API_HASH = "0d273b28f61205ef571461540967255e"  # Apna API Hash yahan daalein
PHONE_NUMBER = "+918920464831"  # Apna Telegram Number yahan daalein

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)
call = PyTgCalls(app)

# YouTube se audio extract karne ka function
def get_audio_url(youtube_url):
    ydl_opts = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "noplaylist": True,
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info["url"]

# /play command (Gaana bajane ke liye)
@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /play [YouTube URL]")
        return

    youtube_url = message.command[1]
    chat_id = message.chat.id

    await message.reply_text("Downloading audio, please wait...")

    audio_url = get_audio_url(youtube_url)

    await call.join_group_call(chat_id, AudioPiped(audio_url, StreamType().local_stream))
    await message.reply_text("Playing song in voice chat!")

# /stop command (Gaana band karne ke liye)
@app.on_message(filters.command("stop"))
async def stop(_, message):
    chat_id = message.chat.id
    await call.leave_group_call(chat_id)
    await message.reply_text("Stopped playing music!")

# /start command
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Hello! I'm a music bot. Use /play [YouTube URL] to play music in voice chat.")

# Stream End Handler
@call.on_stream_end()
async def stream_end_handler(_, update):
    chat_id = update.chat_id
    await call.leave_group_call(chat_id)

# Run Bot
async def main():
    async with app:
        await call.start()
        print("Bot is running...")
        await asyncio.Event().wait()

asyncio.run(main())
