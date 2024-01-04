import re
import api

options = ("similar artists by artist", "similar artists by artists", "similar songs by artists, songs, genres", 
           "query artist genres", "list genres", "exit")

def prompt_user() -> tuple[str]:
    print("Please choose an option:")
    for number, option in enumerate(options):
        print(number, option)
    chosen = input().strip()
    if not re.match(r'\d+', chosen) or int(chosen) not in range(len(options)):
        print("'" + chosen +"'" + " not found")
        return prompt_user()
    else:
        match options[int(chosen)]:
            case "exit":
                return ("exit",)

            case "similar artists by artist":
                print("Enter an artist name:")
                name = input()
                if name == "":
                    print("Invalid name ''")
                    return prompt_user()
                name = api.artist_id(name)
                return ("similar_artists_by_artist", name)

            case "similar artists by artists":
                print("Enter artist names, separated by ',':")
                names = input()
                separated = [x.strip() for x in names.split(',')]
                if any([x == "" for x in separated]):
                    print("Invalid name list '" + names + "'")
                    return prompt_user()
                names = sorted([api.artist_id(name) for name in separated])
                return ("similar_artists_by_artists", names)
            
            case "similar songs by artists, songs, genres":
                remaining = api.MAX_RECOMMENDATIONS
                print(f"Enter up to {remaining} artist names, separated by ',':")
                artists = input()
                separated = [x.strip() for x in artists.split(',')]
                if any([x == "" for x in separated]) and artists != "":
                    print("Invalid artist list '" + artists + "'")
                    return prompt_user()
                artists = sorted([api.artist_id(name) for name in separated]) if artists != "" else []
                if len(artists) > remaining:
                    print("Too many artists entered")
                    return prompt_user()
                remaining -= len(artists)

                print(f"Enter up to {remaining} song names, separated by ',':")
                songs = input()
                separated = [x.strip() for x in songs.split(',')]
                if any([x == "" for x in separated]) and songs != "":
                    print("Invalid song list '" + songs + "'")
                    return prompt_user()
                songs = sorted([api.song_id(name) for name in separated]) if songs != "" else []
                if len(songs) > remaining:
                    print("Too many songs entered")
                    return prompt_user()
                remaining -= len(songs)

                print(f"Enter up to {remaining} genres, separated by ',':")
                genres = input()
                separated = [x.strip() for x in genres.split(',')]
                if any([x == "" for x in separated]) and genres != "":
                    print("Invalid genre list '" + genres + "'")
                    return prompt_user()
                if genres != "":
                    for genre in separated:
                        if api.genre_name(genre.lower()) == "unknown":
                            print(f"Unknown genre '{genre}'")
                            return prompt_user()
                genres = sorted([api.genre_name(name.lower()) for name in separated]) if genres != "" else []
                if len(genres) > remaining:
                    print("Too many genres entered")
                    return prompt_user()

                return ("similar_songs_by_artists_songs_genres", artists, songs, genres)

            case "query artist genres":
                print("Enter an artist name:")
                name = input()
                if name == "":
                    print("Invalid name ''")
                    return prompt_user()
                name = api.artist_id(name)
                return ("query_artist_genres", name)

            case "list genres":
                return ("list_genres",)