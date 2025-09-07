import requests
import pandas as pd

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get_player_stats(username):
    STATS_URL = f"https://api.chess.com/pub/player/{username}/stats"
    response = requests.get(STATS_URL, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to access and retrieve player stats")
        return None


def get_player_archived_games(username):
    ARCHIVED_GAMES_URL = f"https://api.chess.com/pub/player/{username}/games/archives"
    response = requests.get(ARCHIVED_GAMES_URL, headers=HEADERS)

    if response.status_code == 200:
        archives = response.json()["archives"]
        return archives
    else:
        print("Failed to access and retrieve player game archives")
        return []


def get_player_games(archive_url):
    response = requests.get(archive_url, headers=HEADERS)

    if response.status_code == 200:
        games = response.json()
        return games.get("games", [])
    else:
        print("Failed to access and retrieve player games")
        return []


def extract_username(player_field):
    if isinstance(player_field, dict):
        return player_field.get("username", "")
    elif isinstance(player_field, str):
        return player_field.split("/")[-1]
    return ""


def get_player_info(username):
    all_games = []
    archived_games = get_player_archived_games(username)
    for url in archived_games[-4:]:
        requested_games = get_player_games(url)
        for game in requested_games:
            white_player = extract_username(game.get("white"))
            black_player = extract_username(game.get("black"))
            all_games.append(
                {
                    "white": white_player,
                    "black": black_player,
                    "time_class": game.get("time_class"),
                    "white_rating": game.get("white", {}).get("rating"),
                    "black_rating": game.get("black", {}).get("rating"),
                    "result": (
                        game.get("white", {}).get("result")
                        if white_player.lower() == username.lower()
                        else game.get("black", {}).get("result")
                    ),
                    "time_control": game.get("time_control"),
                    "end_time": pd.to_datetime(game.get("end_time"), unit="s"),
                    "pgn": game.get("pgn"),
                }
            )
        return pd.DataFrame(all_games)

