import requests
from base64 import b64encode

ACCESS_URL = "https://accounts.spotify.com/api"
ACCESS_TOKEN = "/token"

API_URL = "https://api.spotify.com"
API_SEARCH = "/search"
API_RELATED_ARTISTS = "/artists/{id}/related-artists"

def get_access_token(client_id, client_secret):
    data = {"grant_type": "client_credentials"}
    encoded_details = b64encode(bytes(client_id + ":" + client_secret, encoding="utf-8")).decode("ascii")
    headers = {"Authorization": "Basic " + encoded_details, "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(ACCESS_URL + ACCESS_TOKEN, data, headers=headers)
    return response.json()['access_token']

def related_artists_by_artist(access_token, name):
    print("Arists similar to", name + ":")
    exit()
    # find an actual artist by this name, using search endpoint

    # get a list of related artists using aptly named endpoint

    # print them for the user 
    ...
