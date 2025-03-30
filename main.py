import os
import logging
import importlib.util
from pyrogram import Client
from config import API_ID, API_HASH, PHONE_NUMBER, PREFIX

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Dominator")

# Initialize the bot
app = Client("Dominator", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

# Dynamically load all plugins from the 'plugins' folder
plugins_folder = 'plugins'

for filename in os.listdir(plugins_folder):
    if filename.endswith('.py') and filename != '__init__.py':
        # Get the name of the module without the .py extension
        plugin_name = filename[:-3]
        
        try:
            # Load the plugin module dynamically
            spec = importlib.util.spec_from_file_location(plugin_name, os.path.join(plugins_folder, filename))
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            logger.info(f"Loaded plugin: {plugin_name}")
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}")

# Run the bot
print("🔥 Dominator Userbot Started!")
logger.info("Dominator Userbot has started!")
app.run()
