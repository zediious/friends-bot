import discord
from discord.ext import commands
from json import loads
from requests import get
from re import compile
from datetime import datetime

from config import settings as SETTINGS
from util import utility as UTILITY

# State bot intents and declare Bot instance
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
friend_bot = commands.Bot(command_prefix='!', description=SETTINGS.DESCRIPTION, intents=intents)

# Define events to listen for
@friend_bot.event
async def on_ready():
    await UTILITY.get_app_list()
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
@friend_bot.tree.command(name="refresh_app_list", description="Forcefully refresh the cached Steam App List. Do not do often!")
@discord.app_commands.describe()
async def gamenews(interaction: discord.Interaction):
    """
    Forcefully refresh the cached Steam App List. Do not do often!
    """
    await UTILITY.get_app_list(delete_old=True)
    await interaction.response.send_message(content="steam_app_list.json has been refreshed. Do not run this command often!")

@friend_bot.tree.command(name="gamenews", description="Gets announcements for a game from Steam News and sends a message with collected news items")
@discord.app_commands.describe(game = "Type the name of a game (be exact!)", amount= "The amount of Announcements you want to fetch")
async def gamenews(interaction: discord.Interaction, game: str, amount: str):
    """
    Gets announcements for a game from Steam API and sends an embed with them
    """
    if int(amount) <= 10:
        embed_list = []
        bad_message_counter = 0
        game_id = await UTILITY.find_game_id(game)
        if game_id == None:
            await interaction.response.send_message(content="A game with the name you provided was not found")
        news_json = loads(get(SETTINGS.STEAM_API_REQUESTS["get_news"].replace('REPLACE_APP', game_id).replace('REPLACE_COUNT', amount)).text)
        REMOVE_TAGS = compile(r'<[^>]+>')
        for message in news_json["appnews"]["newsitems"]:
            message_content = REMOVE_TAGS.sub('', message["contents"])
            if len(message_content) > 500:
                message_content = (message_content[:499] + '..')
            embed_list.append(discord.Embed(title=message["title"], description=f"{message_content}\n\nPosted on `{datetime.fromtimestamp(message['date']).isoformat(' : ', 'hours:minutes')}`", url=message["url"].replace(' ', '')))

        await interaction.response.send_message(content=f"```Last {amount} news items for:``````{game}```" ,embeds=embed_list)
    else: 
        await interaction.response.send_message(content=f"The maximum amount of news items that can be retrieved is 10")

# Run the bot
friend_bot.run(SETTINGS.TOKEN)
