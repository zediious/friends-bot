from os import getenv
from dotenv import load_dotenv

load_dotenv()
# Token defined within .env file in config folder
TOKEN = getenv('DISCORD_TOKEN')
DESCRIPTION = "I do various things!"
DISCORD_GUILD = 215634815469223937

# List of Steam API requests, with placeholders for use in functions
STEAM_API_REQUESTS = {
    "get_all_games": "https://api.steampowered.com/ISteamApps/GetAppList/v2/",
    "get_news": "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=REPLACE_APP&count=REPLACE_COUNT&maxlength=1000000&format=json"
}