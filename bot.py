import asyncio
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
import yt_dlp

# Ultroid Configuration (Replace with your API credentials)
API_ID = 123456  # Replace with your API ID
API_HASH = "your_api_hash"  # Replace with your API Hash
PHONE_NUMBER = "your_phone_number"  # Replace with your phone number

# Initialize Userbot
app = Client("Dominator", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)
call = GroupCallFactory(app).get_group_call()

# Function to Extract Audio from YouTube
async def get_audio_url(youtube_url):
    ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info["url"]

# Play Command
@app.on_message(filters.command("play") & filters.me)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /play [YouTube URL]")
    
    youtube_url = message.command[1]
    chat_id = message.chat.id
    await message.reply_text("Fetching audio...")
    audio_url = await get_audio_url(youtube_url)
    await call.join_group_call(chat_id, audio_url)
    await message.reply_text("Playing in VC!")

# Stop Command
@app.on_message(filters.command("stop") & filters.me)
async def stop(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply_text("Stopped!")

# Start Command
@app.on_message(filters.command("start") & filters.me)
async def start(_, message):
    await message.reply_text("Dominator Userbot is Active! Use /play to play songs in VC.")

async def main():
    async with app:
        await call.start()
        print("Dominator Userbot is Running...")
        await asyncio.Event().wait()

asyncio.run(main())
