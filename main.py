import asyncio
import time
import logging
import random

from pyrogram import Client, filters, enums
from pyrogram.types import InputMediaPhoto

from config import API_ID, API_HASH, STRING_SESSION, PREFIX, IMAGE_URL, OWNER_ID

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Dominator")

# Start Pyrogram Client
app = Client("Dominator", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

start_time = time.time()

# Function to check authorization
def is_authorized(user_id):
    return user_id == OWNER_ID

# Decorator for admin commands
def admin_only(func):
    async def wrapper(client, message):
        if not is_authorized(message.from_user.id):
            await message.reply_text("❌ You are not authorized to use this command!")
            return
        return await func(client, message)
    return wrapper

# Command: Alive
@app.on_message(filters.command("alive", prefixes=PREFIX) & filters.me)
async def alive(client, message):
    try:
        uptime = time.time() - start_time
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}h {minutes}m {seconds}s"

        caption = f"**🔥 Dominator Userbot is Alive!**\n🚀 Uptime: {uptime_str}"
        await message.reply_photo(photo=IMAGE_URL, caption=caption)

        logger.info("Alive command executed")
    except Exception as e:
        logger.error(f"Error in alive command: {e}")
        await message.reply_text("An error occured.")

# Command: Ping
@app.on_message(filters.command("ping", prefixes=PREFIX) & filters.me)
async def ping(client, message):
    try:
        start = time.time()
        reply = await message.reply_text("Pinging...")
        latency = (time.time() - start) * 1000  # Convert to ms

        await reply.delete()
        await message.reply_photo(photo=IMAGE_URL, caption=f"🏓 Pong!\n⚡ Latency: {latency:.2f} ms")

        logger.info("Ping command executed")
    except Exception as e:
        logger.error(f"Error in ping command: {e}")
        await message.reply_text("An error occured.")

# Command: Help
@app.on_message(filters.command("help", prefixes=PREFIX) & filters.me)
async def help_command(client, message):
    try:
        help_text = (
            "✨ **Dominator Userbot Help** ✨\n\n"
            "📌 **Basic Commands:**\n"
            f"- `{PREFIX}alive` → Check bot status\n"
            f"- `{PREFIX}ping` → Check bot latency\n"
            f"- `{PREFIX}help` → Show this help message\n"
            f"- `{PREFIX}hello` → Display Hello Images\n"
            f"- `{PREFIX}game` -> show the game commands\n"
            "\n🔧 **Admin Commands (Owner Only):**\n"
            f"- `{PREFIX}del` → Delete a message\n"
            f"- `{PREFIX}ban` → Ban a user\n"
            f"- `{PREFIX}mute` → Mute a user\n"
            f"- `{PREFIX}unmute` → Unmute a user\n"
            f"- `{PREFIX}promote` → Promote a user\n"
            f"- `{PREFIX}demote` → Demote a user\n"
            "\n🔥 **Enjoy using Dominator!** 🔥"
        )
        await message.reply_photo(photo=IMAGE_URL, caption=help_text)
        logger.info("Help command executed")
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await message.reply_text("An error occured.")

# Command: Game Help
@app.on_message(filters.command("game", prefixes=PREFIX) & filters.me)
async def game_help_command(client, message):
    try:
        game_help_text = (
            "🎮 **Dominator Games** 🎮\n\n"
            "⚔️ **RPG Game:**\n"
            f"- `{PREFIX}rpg start [name]` → Start RPG game\n"
            f"- `{PREFIX}rpg explore [direction]` → Explore\n"
            f"- `{PREFIX}rpg attack` → Attack enemy\n"
            f"- `{PREFIX}rpg info` → Player info\n"
        )
        await message.reply_text(game_help_text)
        logger.info("Game help command executed")
    except Exception as e:
        logger.error(f"Error in game help command: {e}")
        await message.reply_text("An error occured.")

# Command: Hello Images
@app.on_message(filters.command("hello", prefixes=PREFIX) & filters.me)
async def hello(client, message):
    try:
        reply_to_id = message.reply_to_message.id if message.reply_to_message else None
        images = [
            "https://te.legra.ph/file/b86eff074051b0b2d4513.jpg",
            "https://te.legra.ph/file/a679e3d061ac6b349cd60.jpg",
            "https://te.legra.ph/file/96c2b61d6361f112ceac5.jpg",
            "https://te.legra.ph/file/4d0c641e085f7ed15dfec.jpg"
        ]
        HELLO = (
            "╔┓┏╦━╦┓╔┓╔━━╗\n"
            "║┗┛║┗╣┃║┃║X X ║\n"
            "║┏┓║┏╣┗╣┗╣╰╯║\n"
            "╚┛┗╩━╩━╩━╩━━╝\n"
        )
        sent_message = await client.send_photo(message.chat.id, images[0], caption=HELLO, reply_to_message_id=reply_to_id)
        for img in images[1:]:
            await asyncio.sleep(3)
            await sent_message.edit_media(InputMediaPhoto(img))
        await message.delete()
        logger.info("Hello command executed")
    except Exception as e:
        logger.error(f"Error in hello command: {e}")
        await message.reply_text("An error occured.")

# Admin Commands
@app.on_message(filters.command("del", prefixes=PREFIX) & filters.me)
@admin_only
async def delete_message(client, message):
    try:
        if message.reply_to_message:
            await message.reply_to_message.delete()
            await message.delete()
        else:
            await message.reply_text("Reply to a message to delete it.")
        logger.info("del command executed")
    except Exception as e:
        logger.error(f"Error in del command: {e}")
        await message.reply_text("An error occured.")

@app.on_message(filters.command("ban", prefixes=PREFIX) & filters.me)
@admin_only
async def ban_user(client, message):
    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            await client.ban_chat_member(message.chat.id, user_id)
            await message.reply_text("✅ User banned successfully!")
        else:
            await message.reply_text("Reply to a user to ban them.")
        logger.info("ban command executed")
    except Exception as e:
        logger.error(f"Error in ban command: {e}")
        await message.reply_text("An error occured.")

@app.on_message(filters.command("mute", prefixes=PREFIX) & filters.me)
@admin_only
async def mute_user(client, message):
    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            await client.restrict_chat_member(message.chat.id, user_id, permissions=enums.ChatPermissions())
            await message.reply_text("🔇 User muted successfully!")
        else:
            await message.reply_text("Reply to a user to mute them.")
        logger.info("mute command executed")
    except Exception as e:
        logger.error(f"Error in mute command: {e}")
        await message.reply_text("An error occured.")

@app.on_message(filters.command("unmute", prefixes=PREFIX) & filters.me)
@admin_only
async def unmute_user(client, message):
    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            await client.restrict_chat_member(message.chat.id, user_id, permissions=enums.ChatPermissions(can_send_messages=True))
            await message.reply_text("🔊 User unmuted successfully!")
        else:
            await message.reply_text("Reply to a user to unmute them.")
        logger.info("unmute command executed")
    except Exception as e:
        logger.error(f"Error in unmute command: {e}")
        await message.reply_text("An error occured.")

# RPG Game Code
class Character:
    def __init__(self, name, health, attack, defense, mana):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.mana = mana
        self.max_mana = mana
        self.inventory = []
        self.xp = 0
        self.level = 1

    def attack_enemy(self, enemy):
        damage = max(0, self.attack - enemy.defense + random.randint(1, 5))
        enemy.health -= damage
        return damage

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def gain_xp(self, xp):
        self.xp += xp
        if self.xp >= self.level * 100:
            self.level += 1
            self.attack += 5
            self.defense += 3
            self.max_health += 10
            self.health = self.max_health
            return f"{self.name} leveled up! Level: {self.level}"
        return None

class Monster:
    def __init__(self, name, health, attack, defense, level):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level

    def attack_enemy(self, enemy):
        damage = max(0, self.attack - enemy.defense + random.randint(1, 5))
        enemy.health -= damage
        return damage

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

game_state = {
    "player": None,
    "location": "town",
    "current_enemy": None,
}

@app.on_message(filters.command("rpg start", prefixes=PREFIX) & filters.me)
async def rpg_start(client, message):
    try:
        name = message.text.split(" ")[2]
        game_state["player"] = Character(name, 100, 10, 5, 50)
        await message.reply_text(f"{name} created! Welcome to the RPG.")
        logger.info("rpg start command executed")
    except Exception as e:
        logger.error(f"Error in rpg start command: {e}")
        await message.reply_text("An error occured.")

@app.on_message(filters.command("rpg explore", prefixes=PREFIX) & filters.me)
async def rpg_explore(client, message):
    try:
        direction = message.text.split(" ")[2]
        if direction == "north":
            game_state["location"] = "forest"
            game_state["current_enemy"] = Monster("Goblin", 50, 8, 3, 1)
            await message.reply_text("You enter the forest and encounter a Goblin!")
        else:
            await message.reply_text("You can only go north.")
        logger.info("rpg explore command executed")
    except Exception as e:
        logger.error(f"Error in rpg explore command: {e}")
        await message.reply_text("An error occured.")

@app.on_message(filters.command("rpg attack", prefixes=PREFIX) & filters.me)
async def rpg_attack(client, message):
    try:
        if game_state["current_enemy"]:
            player = game_state["player"]
            enemy = game_state["current_enemy"]
            damage = player.attack_enemy(enemy)
            enemy_damage = enemy.attack_enemy(player)
            player.take_damage(enemy_damage)

            if enemy.health <= 0:
                xp = enemy.level * 50
                level_up_message = player.gain_xp(xp)
                game_state["current_enemy"] = None
                result = f"You dealt {damage} damage. Goblin defeated! You gained {xp} XP."
                if level_up_message:
                    result += f"\n{level_up_message}"
                await message.reply_text(result)
            else:
                await message.reply_text(f"You dealt {damage} damage. Goblin dealt {enemy_damage} damage. Your health: {player.health}")
        else:
            await message.reply_text("No enemy to attack.")
        logger.info("rpg attack command executed")
    except Exception as e:
        logger.error(f"Error in rpg attack command: {e}")
        await message.reply_text("An error occured.")

@app.on_message(filters.command("rpg info", prefixes=PREFIX) & filters.me)
async def rpg_info(client, message):
    try:
        if game_state["player"]:
            player = game_state["player"]
            await message.reply_text(f"Name: {player.name}\nHealth: {player.health}/{player.max_health}\nAttack: {player.attack}\nDefense: {player.defense}\nLevel: {player.level}\nXP: {player.xp}")
        else:
            await message.reply_text("No player created. Use !rpg start [name]")
        logger.info("rpg info command executed")
    except Exception as e:
        logger.error(f"Error in rpg info command: {e}")
        await message.reply_text("An error occured.")

# New command: calculator
@app.on_message(filters.command("calc", prefixes=PREFIX) & filters.me)
async def calculator(client, message):
    try:
        expression = message.text.split(" ", 1)[1]
        result = eval(expression)
        await message.reply_text(f"Result: {result}")
        logger.info("calc command executed")
    except (IndexError, SyntaxError, NameError) as e:
        await message.reply_text(f"Invalid expression: {e}")
    except Exception as e:
        logger.error(f"Error in calc command: {e}")
        await message.reply_text("An error occured.")

loop = asyncio.get_event_loop()
app.run()