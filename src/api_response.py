import requests

# Cache to store UUID -> player name mappings
uuid_cache = {}

def top_cleaner(data, removal: str = "heroes"):
    for entry in data:
        entry.pop(removal, None)
    
    return data
    
def get_top_by(sort: str = "kills"):
    return requests.get("https://api.hglabor.de/stats/FFA/top?sort=" + sort).json()


def get_minecraft_username(uuid: str) -> str:
    # Check if the UUID is already cached
    if uuid in uuid_cache:
        return uuid_cache[uuid]
    
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        player_name = data["name"]
        # Cache the result for future use
        uuid_cache[uuid] = player_name
        return player_name
    else:
        return None  # Return None if there's an error fetching the name

def add_player_names_to_list(player_list):
    for player in player_list:
        uuid = player.get("playerId")
        if uuid:
            player_name = get_minecraft_username(uuid)
            player["playerName"] = player_name if player_name else "Unknown"
    return player_list

print(add_player_names_to_list(top_cleaner(get_top_by())))
