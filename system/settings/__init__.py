import json

json_data = {}


def update():
    global json_data
    with open("settings.json") as f:
        json_data = json.loads(f.read())


def save():
    with open("settings.json", "w") as f:
        f.write(json.dumps(json_data))