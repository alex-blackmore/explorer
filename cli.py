import re

options = ("exit", "related artists by artist")

def prompt_user():
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
                exit()
            case "related artists by artist":
                print("Enter an artist name")
                name = input()
                return ("related_artists_by_artist", name)