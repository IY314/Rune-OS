import importlib, os


def run(app_name):
    app = importlib.import_module("apps." + app_name)
    app.launch()