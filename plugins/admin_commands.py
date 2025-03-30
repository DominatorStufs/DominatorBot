from pyrogram import Client, filters
from config import PREFIX  # Import PREFIX from config

# Logging Setup
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Dominator")

# ADMIN: Delete Messages (reply to a message)
@app.on_message(filters.command(["del"], prefixes=[PREFIX]) & filters.reply & filters.me)
def delete_message(client, message):
    try:
        message.reply_to_message.delete()
        message.delete()
        message.reply_text("✅ Message Deleted!")
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")
    logger.info("Delete command executed")

# ADMIN: Ban User (reply to a message)
@app.on_message(filters.command(["ban"], prefixes=[PREFIX]) & filters.reply & filters.me)
def ban_user(client, message):
    try:
        client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        message.reply_text("❌ User Banned!")
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")
    logger.info("Ban command executed")

# ADMIN: Mute User (reply to a message)
@app.on_message(filters.command(["mute"], prefixes=[PREFIX]) & filters.reply & filters.me)
def mute_user(client, message):
    try:
        client.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, permissions={})
        message.reply_text("🔇 User Muted!")
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")
    logger.info("Mute command executed")

# ADMIN: Unmute User (reply to a message)
@app.on_message(filters.command(["unmute"], prefixes=[PREFIX]) & filters.reply & filters.me)
def unmute_user(client, message):
    try:
        client.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, permissions=None)
        message.reply_text("🔊 User Unmuted!")
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")
    logger.info("Unmute command executed")

# ADMIN: Promote User (reply to a message)
@app.on_message(filters.command(["promote"], prefixes=[PREFIX]) & filters.reply & filters.me)
def promote_user(client, message):
    try:
        client.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_manage_chat=True)
        message.reply_text("🌟 User Promoted!")
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")
    logger.info("Promote command executed")

# ADMIN: Demote User (reply to a message)
@app.on_message(filters.command(["demote"], prefixes=[PREFIX]) & filters.reply & filters.me)
def demote_user(client, message):
    try:
        client.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_manage_chat=False)
        message.reply_text("⬇️ User Demoted!")
    except Exception as e:
        message.reply_text(f"❌ Error: {e}")
    logger.info("Demote command executed")
