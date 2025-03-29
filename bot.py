from pyrogram import Client, filters
import os

# Bot Configuration
API_ID = int(os.getenv("API_ID", "6301598"))  # Replace with your API ID
API_HASH = os.getenv("API_HASH", "0d273b28f61205ef571461540967255e")  # Replace with your API Hash
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "+918920464831")  # Your phone number

# Initialize the bot
app = Client("Dominator", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

@app.on_message(filters.command("start") & filters.me)
def start(client, message):
    message.reply_text("Dominator Userbot is up and running!")

@app.on_message(filters.command("ping") & filters.me)
def ping(client, message):
    message.reply_text("Pong! 🏓")

# Run the bot
print("Dominator Userbot Started!")
app.run()
