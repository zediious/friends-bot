import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from json import dump, dumps, load

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

DESCRIPTION = "I do various things!"
DISCORD_GUILD = 215634815469223937

# State bot intents and declare Bot instance
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
friend_bot = commands.Bot(command_prefix='!', description=DESCRIPTION, intents=intents)

# Define events to listen for
@friend_bot.event
async def on_ready():
    print(f'Logged in as {friend_bot.user} (ID: {friend_bot.user.id})')
    try:
        synced = await friend_bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@friend_bot.event
async def on_message(message):
    pass

@friend_bot.event
async def on_raw_message_edit(message):
    pass

@friend_bot.event
async def on_presence_update(before, after):
    pass

# Define Bot commands
@friend_bot.tree.command(name="gamenews")
@discord.app_commands.describe(key = "Type a game name or app ID")
async def gamenews(interaction: discord.Interaction, key: str):
    pass

# Run the bot
friend_bot.run(TOKEN)
