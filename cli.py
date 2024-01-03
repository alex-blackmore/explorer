import re
import api

options = ("exit", "related artists by artist", "related artists by artists")

def prompt_user() -> tuple[str]:
    print("Please choose an option")
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
            case "related artists by artist":
                print("Enter an artist name:")
                name = input()
                if name == "":
                    print("Invalid name ''")
                    return prompt_user()
                name = api.artist_id(name)
                return ("related_artists_by_artist", name)
            case "related artists by artists":
                print("Enter artist names, seperated by ','")
                names = input()
                seperated = [x.strip() for x in names.split(',')]
                if any([x == "" for x in seperated]):
                    print("Invalid name list '" + names + "'")
                    return prompt_user()
                names = sorted([api.artist_id(name) for name in seperated])
                return ("related_artists_by_artists", names)