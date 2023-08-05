import os
import textwrap
import json

def main():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "filenames.json")
    ) as file:
        filesnames = json.load(file)

    files = []
    replacelist = []
    with os.scandir(".") as it:
        for entry in it:
            name = entry.name
            if entry.is_dir():
                name += "/"
                replacelist.append([name, "\033[92m\033[4m" + name + "\033[0m"])
            elif name.lower().startswith("readme") or name in filesnames["immediate"]:
                replacelist.append([name, "\033[1;33m" + name + "\033[0m"])
            elif name.endswith(tuple(filesnames["image"])):
                replacelist.append([name, "\033[0;35m" + name + "\033[0m"])
            elif name.endswith(tuple(filesnames["video"])):
                replacelist.append([name, "\033[0;36m" + name + "\033[0m"])
            elif name.endswith(tuple(filesnames["music"])):
                replacelist.append([name, "\033[0;34m" + name + "\033[0m"])
            elif name.endswith(tuple(filesnames["document"])):
                replacelist.append([name, "\033[1;34m" + name + "\033[0m"])
            elif name.endswith(tuple(filesnames["compressed"])):
                replacelist.append([name, "\033[1;35m\033[4m" + name + "\033[0m"])
            files.append(name)

    width = os.get_terminal_size().columns // 23 * 23
    text = "\n".join(
        textwrap.wrap(
            "\t".join(files),
            width=width,
            break_on_hyphens=False,
            break_long_words=False,
            tabsize=23,
        )
    )
    for pair in replacelist:
        text = text.replace(pair[0], pair[1])

    print(text)

if __name__ == "__main__":
    main()
