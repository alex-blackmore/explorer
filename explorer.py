#!/usr/bin/env python3
from env import load_env, read_env
from cli import prompt_user
import api
import sys
import info

if __name__ == "__main__":
    load_env(".env")

    client_id = read_env("CLIENT_ID")
    client_secret = read_env("CLIENT_SECRET")

    access_token = api.get_access_token(client_id, client_secret)
    info.headers = {"Authorization": "Bearer " + access_token}
    
    while True:
        action = prompt_user()
        args = action[1:]
        match action[0]:
            case "exit":
                sys.exit(0)
            case "similar_artists_by_artist":
                api.similar_artists_by_artist(*args, output=True)
            case "similar_artists_by_artists":
                api.similar_artists_by_artists(*args, output=True)
            case "similar_songs_by_artists_songs_genres":
                api.similar_songs_by_artists_songs_genres(*args, output=True)
            case "query_artist_genres":
                api.query_artist_genres(*args)
            case "list_genres":
                api.list_genres(output=True)