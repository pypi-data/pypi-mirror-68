import json

with open("betterls/filenames.json") as file:
    filesnames = json.load(file)

for a, list in filesnames.items():
    newlist = []
    for extension in list:
        newlist.append("." + extension)
    print("[\"" + '", "'.join(newlist) + "\"],")