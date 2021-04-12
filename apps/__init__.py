import importlib, os, json

json_data = {}


def update():
    global json_data
    with open("system/info.json") as f:
        json_data = json.loads(f.read())


def run(app_name):
    update()
    try:
        app = importlib.import_module(f"apps.user.{json_data['CURRENT']['username']}.{app_name}")
        app.launch()
    except ModuleNotFoundError:
        app = importlib.import_module(f"apps.public.{app_name}")
        app.launch()
