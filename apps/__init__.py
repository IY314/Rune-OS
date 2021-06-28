import os
import sys
import importlib
from system import utils

data = utils.File('system/accounts.json')


def run(app_name):
    data.update()
    try:
        app = importlib.import_module(f'apps.private.{data.data["CURRENT"]["username"]}.{app_name}')
        app.launch()
    except ModuleNotFoundError:
        app = importlib.import_module(f'apps.public.{app_name}')
        app.launch()
