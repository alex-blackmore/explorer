import requests
import sys
import info
from base64 import b64encode
from helpers import cache, print_separator

ACCESS_URL = "https://accounts.spotify.com/api"
ACCESS_TOKEN = "/token"

API_URL = "https://api.spotify.com/v1"
API_SEARCH = "/search"
API_RELATED_ARTISTS_1 = "/artists/"
API_RELATED_ARTISTS_2 = "/related-artists"
API_ARTIST = "/artists/"
API_GENRES = "/recommendations/available-genre-seeds"
API_SONG = "/tracks/"
API_RECOMMENDATIONS = "/recommendations"
MAX_RECOMMENDATIONS = 5

def get_access_token(client_id: str, client_secret: str) -> str:
    data = {"grant_type": "client_credentials"}
    encoded_details = b64encode(bytes(client_id + ":" + client_secret, encoding="utf-8")).decode("ascii")
    headers = {"Authorization": "Basic " + encoded_details, "Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(ACCESS_URL + ACCESS_TOKEN, data, headers=headers)
    return response.json()['access_token']

@cache
def artist_id(name: str) -> str:
    params = {"q": name, "type": "artist", "limit": "1"}
    response = requests.get(API_URL + API_SEARCH, params, headers=info.headers)
    results = response.json()["artists"]["items"]

    if not results:
        print(f"Couldn't find artist for '{name}'")
        sys.exit(1)

    return results[0]["id"]

@cache
def artist_info(id: str) -> dict:
    response = requests.get(API_URL + API_ARTIST + id, headers=info.headers)
    return response.json()

@cache
def song_id(name: str) -> str:
    params = {"q": name, "type": "track", "limit": "1"}
    response = requests.get(API_URL + API_SEARCH, params, headers=info.headers)
    results = response.json()["tracks"]["items"]

    if not results:
        print(f"Couldn't find song for '{name}'")
        sys.exit(1)

    return results[0]["id"]

@cache
def song_info(id: str) -> dict:
    response = requests.get(API_URL + API_SONG + id, headers=info.headers)
    return response.json()

@cache
def genre_name(name: str) -> str:
    genres = list_genres(output=False)
    
    if name not in genres:
        return "unknown"
    
    return name

@cache
def similar_artists_by_artist(id: str, output: bool) -> dict:
    results = artist_info(id)
    
    if output:
        print_separator()
        print("Artists similar to", results["name"] + ":")
    
    url = API_URL + API_RELATED_ARTISTS_1 + results["id"] + API_RELATED_ARTISTS_2
    params = {"id": results["id"]}
    response = requests.get(url, params, headers=info.headers)
    
    results = response.json()["artists"]
    if output:
        for entry in results:
            print(entry["name"])
        print_separator()

    return results

@cache
def similar_artists_by_artists(ids: str, output: bool) -> None:
    results = {}

    for id in ids:
        for entry in similar_artists_by_artist(id, output=False):
            if entry["name"] in results:
                results[entry["name"]] += 1
            else:
                results[entry["name"]] = 1

    if output:
        print_separator()
        print("Artists similar to ", end="")
        print(", ".join([artist_info(id)["name"] for id in ids]) + ":")

        for artist in sorted(results, key=lambda x : results[x], reverse=True):
            print(results[artist], artist)
        print_separator()
    return results

@cache
def query_artist_genres(id: str) -> None:
    print_separator()
    for genre in artist_info(id)["genres"]:
        print(genre)
    print_separator()

@cache
def list_genres(output: bool) -> list[str]:
    response = requests.get(API_URL + API_GENRES, headers=info.headers)
    results = response.json()["genres"]
    if output:
        print_separator()
        for genre in results:
            print(genre)
        print_separator()
    return results

@cache
def similar_songs_by_artists_songs_genres(artist_ids: tuple[str], song_ids: tuple[str], genre_names: tuple[str], output: bool) -> None:
    params = {}
    if len(artist_ids) > 0:
        params["seed_artists"] = ",".join(artist_ids)
    if len(song_ids) > 0:
        params["seed_tracks"] = ",".join(song_ids)
    if len(genre_names) > 0:
        params["seed_genres"] = ",".join(genre_names)
    response = requests.get(API_URL + API_RECOMMENDATIONS, params, headers=info.headers)
    results = response.json()["tracks"]
    if output:
        print_separator()
        print("Similar songs:")
        for song in results:
            print(song["name"], "by", ", ".join([artist["name"] for artist in song["artists"]]))
        print_separator()
    return results