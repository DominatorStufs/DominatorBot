import asyncio
from pyrogram import Client, filters

# Ultroid Configuration (Replace with your API credentials)
API_ID = 123456  # Replace with your API ID
API_HASH = "your_api_hash"  # Replace with your API Hash
PHONE_NUMBER = "your_phone_number"  # Replace with your phone number

# Initialize Userbot
app = Client("Dominator", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

# Start Command
@app.on_message(filters.command("start") & filters.me)
async def start(_, message):
    await message.reply_text("Dominator Userbot is Active!")

# Ping Command
@app.on_message(filters.command("ping") & filters.me)
async def ping(_, message):
    await message.reply_text("Pong!")

# Echo Command
@app.on_message(filters.command("echo") & filters.me)
async def echo(_, message):
    text = " ".join(message.command[1:])
    if text:
        await message.reply_text(text)
    else:
        await message.reply_text("Usage: /echo [your text]")

# ID Command
@app.on_message(filters.command("id") & filters.me)
async def get_id(_, message):
    await message.reply_text(f"Chat ID: `{message.chat.id}`\nUser ID: `{message.from_user.id}`")

# Delete Messages
@app.on_message(filters.command("del") & filters.me)
async def delete_msg(_, message):
    if message.reply_to_message:
        await message.reply_to_message.delete()
        await message.delete()
    else:
        await message.reply_text("Reply to a message to delete it.")

# Broadcast Message
@app.on_message(filters.command("broadcast") & filters.me)
async def broadcast(_, message):
    text = " ".join(message.command[1:])
    if text:
        async for dialog in app.get_dialogs():
            try:
                await app.send_message(dialog.chat.id, text)
            except:
                continue
        await message.reply_text("Broadcast sent successfully!")
    else:
        await message.reply_text("Usage: /broadcast [your message]")

# Ban User
@app.on_message(filters.command("ban") & filters.me)
async def ban(_, message):
    if message.reply_to_message:
        await message.chat.ban_member(message.reply_to_message.from_user.id)
        await message.reply_text("User banned!")
    else:
        await message.reply_text("Reply to a user to ban them.")

# Unban User
@app.on_message(filters.command("unban") & filters.me)
async def unban(_, message):
    if len(message.command) > 1:
        user_id = int(message.command[1])
        await message.chat.unban_member(user_id)
        await message.reply_text("User unbanned!")
    else:
        await message.reply_text("Usage: /unban [user_id]")

# Promote User
@app.on_message(filters.command("promote") & filters.me)
async def promote(_, message):
    if message.reply_to_message:
        await message.chat.promote_member(message.reply_to_message.from_user.id, can_manage_chat=True)
        await message.reply_text("User promoted!")
    else:
        await message.reply_text("Reply to a user to promote them.")

# Demote User
@app.on_message(filters.command("demote") & filters.me)
async def demote(_, message):
    if message.reply_to_message:
        await message.chat.promote_member(message.reply_to_message.from_user.id, can_manage_chat=False)
        await message.reply_text("User demoted!")
    else:
        await message.reply_text("Reply to a user to demote them.")

# AFK Mode
AFK_STATUS = {}
@app.on_message(filters.command("afk") & filters.me)
async def afk(_, message):
    AFK_STATUS[message.from_user.id] = True
    await message.reply_text("AFK mode activated!")

@app.on_message(filters.private & filters.incoming)
async def afk_reply(_, message):
    if message.from_user.id in AFK_STATUS:
        await message.reply_text("User is currently AFK.")

@app.on_message(filters.command("back") & filters.me)
async def back(_, message):
    if message.from_user.id in AFK_STATUS:
        del AFK_STATUS[message.from_user.id]
        await message.reply_text("AFK mode deactivated!")

async def main():
    async with app:
        print("Dominator Userbot is Running...")
        await asyncio.Event().wait()

asyncio.run(main())
