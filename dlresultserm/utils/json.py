import json
import os
from pathlib import Path


def save_to_json_file(data, filename):
    """Save to JSON file

    :data: data from scrapersave
    :filename: filename to save in
    :returns: None

    """
    directory = os.path.dirname(filename)
    Path(directory).mkdir(parents=True, exist_ok=True)

    with open(filename, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    return


def get_json_from_file(filename):

    with open(filename, 'r', encoding='utf8') as json_file:
        obj = json.loads(json_file.read())
    return obj


if __name__ == "__main__":

    data = get_json_from_file("output/results.json")
    print(data)
