#!/usr/bin/env python3
from env import load_env, read_env
from cli import prompt_user
import api

if __name__ == "__main__":
    load_env(".env")

    client_id = read_env("CLIENT_ID")
    client_secret = read_env("CLIENT_SECRET")

    access_token = api.get_access_token(client_id, client_secret)

    action = prompt_user()

    match action[0]:
        case "related_artists_by_artist": 
            api.related_artists_by_artist(access_token, *action[1:])