from json import load

async def find_game_id(game_arg):
    """
    Given a game's name, find that game's Steam App ID
    """
    with open('steam_app_list.json', "r") as app_list:
        app_json = load(app_list)
        for game in app_json["applist"]["apps"]:
            if game_arg == str(game["name"]):
                return str(game["appid"])