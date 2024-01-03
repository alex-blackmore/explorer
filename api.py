import requests
import sys
from base64 import b64encode

ACCESS_URL = "https://accounts.spotify.com/api"
ACCESS_TOKEN = "/token"

API_URL = "https://api.spotify.com/v1"
API_SEARCH = "/search"
API_RELATED_ARTISTS_1 = "/artists/"
API_RELATED_ARTISTS_2 = "/related-artists"

def get_access_token(client_id: str, client_secret: str) -> str:
    data = {"grant_type": "client_credentials"}
    encoded_details = b64encode(bytes(client_id + ":" + client_secret, encoding="utf-8")).decode("ascii")
    headers = {"Authorization": "Basic " + encoded_details, "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(ACCESS_URL + ACCESS_TOKEN, data, headers=headers)
    return response.json()['access_token']

def related_artists_by_artist(headers: dict[str, str], name: str) -> None:
    # find an actual artist by this name, using search endpoint
    params = {"q": name, "type": "artist", "limit": "1"}
    response = requests.get(API_URL + API_SEARCH, params, headers=headers)
    results = response.json()["artists"]["items"]
    if not results:
        print(f"Couldn't find matching artist for '{name}'")
        sys.exit(1)
    actual_name = results[0]["name"]
    print("Arists similar to", actual_name + ":")
    artist_id = results[0]["id"]
    # get a list of related artists, using related artists endpoint
    url = API_URL + API_RELATED_ARTISTS_1 + artist_id + API_RELATED_ARTISTS_2
    params = {"id": artist_id}
    response = requests.get(url, params, headers=headers)
    # print them for the user 
    results = response.json()["artists"]
    for entry in results:
        print(entry["name"])
