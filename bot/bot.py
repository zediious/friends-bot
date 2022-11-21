import discord
from discord.ext import commands
from os.path import getsize
from json import dumps, loads
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
    try:
        with open('steam_app_list.json', "r+") as app_list:
            if getsize('steam_app_list.json') < 1024:
                app_json = loads(get(SETTINGS.STEAM_API_REQUESTS["get_all_games"]).text)
                app_list.write(dumps(app_json, indent=4))
                app_list.close()

    except:
        create_file = open('steam_app_list.json', 'w')
        create_file.close()
        with open('steam_app_list.json', "r+") as app_list:
            if getsize('steam_app_list.json') < 1024:
                app_json = loads(get(SETTINGS.STEAM_API_REQUESTS["get_all_games"]).text)
                app_list.write(dumps(app_json, indent=4))
                app_list.close()
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
@discord.app_commands.describe(game = "Type the name of a game (be exact!)", amount= "The amount of Announcements you want to fetch")
async def gamenews(interaction: discord.Interaction, game: str, amount: str):
    """
    Gets announcements for a game from Steam API and sends an embed with them
    """
    embed_list = []
    game_id = await UTILITY.find_game_id(game)
    if game_id == None:
        await interaction.response.send_message(content="A game with the name you provided was not found")
    news_json = loads(get(SETTINGS.STEAM_API_REQUESTS["get_news"].replace('REPLACE_APP', game_id).replace('REPLACE_COUNT', amount)).text)
    header = discord.Embed(title=f"News for: {game}", url=SETTINGS.STEAM_API_REQUESTS["get_news"].replace('REPLACE_APP', game_id).replace('REPLACE_COUNT', amount))
    embed_list.append(header)
    REMOVE_TAGS = compile(r'<[^>]+>')
    for message in news_json["appnews"]["newsitems"]:
        message_content = REMOVE_TAGS.sub('', message["contents"])
        embed_list.append(discord.Embed(title=message["title"], description=f"{message_content}\n\nPosted on `{datetime.fromtimestamp(message['date']).isoformat('#', 'hours')}`", url=message["url"]))

    await interaction.response.send_message(embeds=embed_list)

# Run the bot
friend_bot.run(SETTINGS.TOKEN)
