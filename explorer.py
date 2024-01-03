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
            case "related_artists_by_artist":
                api.related_artists_by_artist(*args, output=True)
            case "related_artists_by_artists":
                api.related_artists_by_artists(*args, output=True)