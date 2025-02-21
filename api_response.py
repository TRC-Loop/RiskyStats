import requests
import csv
import os

# Cache to store UUID -> player name mappings
uuid_cache = {}

# Check if the CSV file exists to read it
def load_cache_from_csv():
    if os.path.exists('uuid_cache.csv'):
        with open('uuid_cache.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                if row:
                    uuid_cache[row[0]] = row[1]

# Function to get the Minecraft username for a UUID
def get_minecraft_username(uuid: str) -> str:
    # Check if the UUID is in the cache first
    if uuid in uuid_cache:
        return uuid_cache[uuid]
    
    # Check if the UUID is in the CSV file
    with open('uuid_cache.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            if row[0] == uuid:
                # Add to in-memory cache for future use
                uuid_cache[uuid] = row[1]
                return row[1]
    
    # If not found in cache or CSV, call the API
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        player_name = data["name"]
        # Cache the result and write it to CSV
        uuid_cache[uuid] = player_name
        append_uuids_to_csv([[uuid, player_name]])  # Write new entry to CSV
        return player_name
    else:
        return None  # Return None if there's an error fetching the name

# Function to add player names to the list
def add_player_names_to_list(player_list):
    new_entries = []
    
    for player in player_list:
        uuid = player.get("playerId")
        if uuid:
            player_name = get_minecraft_username(uuid)
            player["playerName"] = player_name if player_name else "Unknown"
    
    return player_list

# Function to append new entries to the CSV file
def append_uuids_to_csv(new_entries):
    with open('uuid_cache.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Only append the new entries to the CSV
        for entry in new_entries:
            writer.writerow(entry)

# Function to clean the top player list
def top_cleaner(data, removal: str = "heroes"):
    for entry in data:
        entry.pop(removal, None)
    
    return data

def getPlayer(uuid: str):
    request = requests.get("https://api.hglabor.de/stats/FFA/" + uuid)
    return request.json()

def getPlayerFull(uuid):
    plr_base = getPlayer(uuid)
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(url)
    
    plr_base["playerName"] = response.json()["name"]
    return plr_base

# Function to get top players by a specified sort parameter
def get_top_by(sort: str = "kills"):
    return requests.get(f"https://api.hglabor.de/stats/FFA/top?sort={sort}").json()

# Load the cache from CSV if available
load_cache_from_csv()