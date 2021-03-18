import shutil, os

def install(app_name, path="apps"):
    apps = os.listdir("extensions")
    installed = os.listdir(path)
    a = 0
    while a < len(installed):
        if installed[a] in ("__init__.py", "__pycache__", "user"):
            del installed[a]
        a += 1
    a = 0
    while a < len(apps):
        if apps[a] in ["__init__.py", "__pycache__"] + installed:
            del apps[a]
        a += 1
    del a
    for a in apps:
        if app_name == a:
            shutil.copytree(os.path.join("extensions", app_name), os.path.join(path, app_name))
            break
    
    else:
        raise ModuleNotFoundError("App not found or installed.")


def uninstall(app_name, path):
    apps = os.listdir(path)
    a = 0
    while a < len(apps):
        if apps[a] in ("__init__.py", "__pycache__", "user"):
            del apps[a]
        a += 1
    del a
    for a in apps:
        if app_name == a:
            shutil.rmtree(os.path.join(path, app_name))
            break

    else:
        raise ModuleNotFoundError("App not found.")


def search(app_name, user_path):
    apps = os.listdir("apps")
    a = 0
    while a < len(apps):
        if apps[a] in ("__init__.py", "__pycache__", "user"):
            del apps[a]
        a += 1
    user_apps = os.listdir(user_path)
    a = 0
    while a < len(user_apps):
        if user_apps[a] in ("__init__.py", "__pycache__"):
            del user_apps[a]
        a += 1
    del a
    for a in apps:
        if app_name == a:
            return "public"
    
    for a in user_apps:
        if app_name == a:
            return "local"
    else:
        raise ModuleNotFoundError("App not found.")
