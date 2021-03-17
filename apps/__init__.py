import importlib, os, json

json_data = {}


def save():
    with open("system/info.json", "w") as f:
        f.write(json.dumps(json_data))


def update():
    global json_data
    with open("system/info.json") as f:
        json_data = json.loads(f.read())


def run(app_name):
    update()
    app = importlib.import_module(f"apps.user.{json_data['CURRENT']['username']}.{app_name}")
    app.launch()
