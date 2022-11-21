from json import load, dumps, loads
from os.path import getsize
from requests import get

from config import settings as SETTINGS

async def get_app_list(delete_old=False):
    """
    If steam_app_list.json is empty or does not exist, get the data from
    Steam API and save. If `delete_old` parameter is passes as True, new data
    will be fetched no matter the current state of steam_app_list.json
    """
    try:
        with open('steam_app_list.json', "r+") as app_list:
            if getsize('steam_app_list.json') < 1024 or delete_old == True:
                app_json = loads(get(SETTINGS.STEAM_API_REQUESTS["get_all_games"]).text)
                app_list.write(dumps(app_json, indent=4))
                app_list.close()

    except:
        create_file = open('steam_app_list.json', 'w')
        create_file.close()
        with open('steam_app_list.json', "r+") as app_list:
            if getsize('steam_app_list.json') < 1024 or delete_old == True:
                app_json = loads(get(SETTINGS.STEAM_API_REQUESTS["get_all_games"]).text)
                app_list.write(dumps(app_json, indent=4))
                app_list.close()

async def find_game_id(game_arg):
    """
    Given a game's name, find that game's Steam App ID
    """
    with open('steam_app_list.json', "r") as app_list:
        app_json = load(app_list)
        for game in app_json["applist"]["apps"]:
            if game_arg == str(game["name"]):
                return str(game["appid"])