from pyrogram import Client, filters
import os
import asyncio
import time
import logging
import yt_dlp
from config import API_ID, API_HASH, PHONE_NUMBER
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Dominator")

# Initialize the bot
app = Client("Dominator", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)
vc = PyTgCalls(app)
start_time = time.time()

auto_replies = {}
current_chat = None

# START Command
@app.on_message(filters.command(["start"], prefixes=["."]) & filters.me)
def start(client, message):
    uptime = time.time() - start_time
    hours, remainder = divmod(int(uptime), 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"
    message.reply_text(f"**🔥 Dominator Userbot is Running!**\n🚀 Uptime: {uptime_str}")
    logger.info("Start command executed")

# PING Command
@app.on_message(filters.command(["ping"], prefixes=["."]) & filters.me)
def ping(client, message):
    start = time.time()
    reply = message.reply_text("Pinging...")
    latency = (time.time() - start) * 1000  # Convert to ms
    reply.edit_text(f"🏓 Pong!\n⚡ Latency: {latency:.2f} ms")
    logger.info("Ping command executed")

# HELP Command
@app.on_message(filters.command(["help"], prefixes=["."]) & filters.me)
def help_command(client, message):
    help_text = (
        "✨ **Dominator Userbot Help** ✨\n\n"
        "📌 **Commands:**\n"
        "- `.start` → Check bot status\n"
        "- `.ping` → Check bot latency\n"
        "- `.ytmp3 link` → Download YouTube audio\n"
        "- `.ytmp4 link` → Download YouTube video\n"
        "- `.play song_name_or_link` → Play music in VC\n"
        "- `.pause` → Pause music\n"
        "- `.resume` → Resume music\n"
        "- `.stop` → Stop music\n"
        "- `.setreply trigger=text` → Set auto-reply\n"
        "- `.delreply trigger` → Delete auto-reply\n"
        "\n🔥 **Enjoy using Dominator!** 🔥"
    )
    client.send_message(message.chat.id, help_text)
    logger.info("Help command executed")

# YOUTUBE DOWNLOADER
@app.on_message(filters.command(["ytmp3", "ytmp4"], prefixes=["."]) & filters.me)
def download_youtube(client, message):
    if len(message.command) < 2:
        message.reply_text("❌ Please provide a YouTube link!")
        return
    
    url = message.command[1]
    format_type = "mp3" if message.command[0] == ".ytmp3" else "mp4"
    message.reply_text(f"🔄 Downloading {format_type.upper()}...")
    
    options = {
        "format": "bestaudio/best" if format_type == "mp3" else "bestvideo+bestaudio",
        "outtmpl": f"downloads/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }] if format_type == "mp3" else []
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    
    for file in os.listdir("downloads"):
        if file.endswith(".mp3") or file.endswith(".mp4"):
            client.send_document(message.chat.id, f"downloads/{file}", caption="✅ Download Complete!")
            os.remove(f"downloads/{file}")
            break

# MUSIC PLAYER
@app.on_message(filters.command("play", prefixes=["."]) & filters.me)
def play_music(client, message):
    global current_chat
    if len(message.command) < 2:
        message.reply_text("❌ Provide a song name or YouTube link!")
        return
    
    url = message.command[1]
    chat_id = message.chat.id
    current_chat = chat_id
    
    options = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/music.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    
    for file in os.listdir("downloads"):
        if file.startswith("music") and file.endswith(".mp3"):
            vc.join_group_call(chat_id, AudioPiped(f"downloads/{file}"))
            message.reply_text("🎵 Playing Music in VC!")
            break

@app.on_message(filters.command("pause", prefixes=["."]) & filters.me)
def pause_music(client, message):
    if current_chat:
        vc.pause_stream(current_chat)
        message.reply_text("⏸ Music Paused!")

@app.on_message(filters.command("resume", prefixes=["."]) & filters.me)
def resume_music(client, message):
    if current_chat:
        vc.resume_stream(current_chat)
        message.reply_text("▶ Music Resumed!")

@app.on_message(filters.command("stop", prefixes=["."]) & filters.me)
def stop_music(client, message):
    global current_chat
    if current_chat:
        vc.leave_group_call(current_chat)
        message.reply_text("⏹ Music Stopped!")
        current_chat = None

# Run the bot
print("🔥 Dominator Userbot Started!")
logger.info("Dominator Userbot has started!")
vc.start()
app.run()
