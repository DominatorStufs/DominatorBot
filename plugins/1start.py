from pyrogram import Client, filters
import time
from config import PREFIX  # Prefix import from config

# Logging Setup
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Dominator")

start_time = time.time()

# START Command
@app.on_message(filters.command(["start"], prefixes=[PREFIX]) & filters.me)
def start(client, message):
    uptime = time.time() - start_time
    hours, remainder = divmod(int(uptime), 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"
    message.reply_text(f"**🔥 Dominator Userbot is Running!**\n🚀 Uptime: {uptime_str}")
    logger.info("Start command executed")

# PING Command
@app.on_message(filters.command(["ping"], prefixes=[PREFIX]) & filters.me)
def ping(client, message):
    start = time.time()
    reply = message.reply_text("Pinging...")
    latency = (time.time() - start) * 1000  # Convert to ms
    reply.edit_text(f"🏓 Pong!\n⚡ Latency: {latency:.2f} ms")
    logger.info("Ping command executed")

# HELP Command
@app.on_message(filters.command(["help"], prefixes=[PREFIX]) & filters.me)
def help_command(client, message):
    help_text = (
        "✨ **Dominator Userbot Help** ✨\n\n"
        "📌 **Commands:**\n"
        f"- `{PREFIX}start` → Check bot status\n"
        f"- `{PREFIX}ping` → Check bot latency\n"
        f"- `{PREFIX}help` → Show this help message\n"
        "\n🔥 **Admin Commands:**\n"
        f"- `{PREFIX}ban [user]` → Ban a user\n"
        f"- `{PREFIX}mute [user]` → Mute a user\n"
        f"- `{PREFIX}unmute [user]` → Unmute a user\n"
        f"- `{PREFIX}promote [user]` → Promote a user\n"
        f"- `{PREFIX}demote [user]` → Demote a user\n"
        f"- `{PREFIX}del` → Delete a message (reply to a message)\n"
        "\n🔥 **Enjoy using Dominator!** 🔥"
    )
    client.send_message(message.chat.id, help_text)
    logger.info("Help command executed")
