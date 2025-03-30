import os
import subprocess
import sys
from pyrogram import Client, filters
from config import API_ID, API_HASH, PHONE_NUMBER, PREFIX

# Logging Setup
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Dominator")

# Initialize the bot
app = Client("Dominator", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

# .update Command: This will pull the latest changes from GitHub and restart the bot
@app.on_message(filters.command(["update"], prefixes=[PREFIX]) & filters.me)
def update(client, message):
    try:
        # GitHub repository URL
        git_repo_url = "https://github.com/DominatorStufs/TryBot.git"  # Replace with your repository URL
        
        # Path where you want the bot files to be cloned
        bot_directory = "/storage/emulated/0/termuxbot/TryBot/plugins"  # Adjust path if needed
        
        # If the directory doesn't exist, clone the repository
        if not os.path.exists(bot_directory):
            os.makedirs(bot_directory)
            subprocess.run(["git", "clone", git_repo_url, bot_directory])
            message.reply_text("📦 **Bot cloned from GitHub!**")
            logger.info("Bot cloned from GitHub")
        
        # Change directory to the bot's directory
        os.chdir(bot_directory)

        # Pull the latest changes from GitHub
        result = subprocess.run(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check if the update was successful
        if result.returncode == 0:
            message.reply_text("📦 **Bot successfully updated!**")
            logger.info("Bot updated successfully")
            # Restart the bot with new updates
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            message.reply_text(f"❌ **Error updating bot: {result.stderr.decode()}**")
            logger.error(f"Error updating bot: {result.stderr.decode()}")
    except Exception as e:
        message.reply_text(f"❌ **An error occurred: {e}**")
        logger.error(f"Error: {e}")

# Run the bot
print("🔥 Dominator Userbot Started!")
logger.info("Dominator Userbot has started!")
app.run()
