import json, time, os, sys, hashlib, shutil
sys.path.append("../")
import apps, extensions
from system import utils

json_data = {}


def update():
    global json_data
    with open("system/info.json") as f:
        json_data = json.loads(f.read())

    del f


def save():
    with open("system/info.json", "w") as f:
        f.write(json.dumps(json_data))


def launch():
    utils.clear_console()
    now = int(time.strftime("%H"))
    if now <= 4 or now > 22:
        tod = "night"
    elif now > 16 and now <= 22:
        tod = "evening"
    elif now > 12 and now <= 16:
        tod = "afternoon"
    elif now > 5 and now <= 12:
        tod = "morning"
    else:
        raise ValueError(f"The time is not handled ({now})!")
    update()
    user = json_data["CURRENT"]["username"]
    print(f"Good {tod}, {user}!")
    while True:
        home(True)


def home(noclear=False):
    global json_data
    if not noclear: utils.clear_console()
    options = "Enter 1 to run an app.\nEnter 2 to delete your account.\nEnter 3 to install an app."
    if json_data["CURRENT"]["has_admin"]:
        options += "\nEnter 4 to clear all accounts."
    options += "\nEnter anything else to logout."
    print(options)
    action = input(">")
    if action == "1":
        run_app()
    elif action == "2":
        delete_account()
    elif action == "3":
        install_app()
    elif action == "4" and json_data["CURRENT"]["has_admin"]:
        delete_all_accounts()
    else:
        logout()


def run_app(noclear=False):
    if not noclear: utils.clear_console()
    public_apps = os.listdir("apps")
    i = 0
    while i < len(public_apps):
        if public_apps[i] in ("__init__.py", "__pycache__", "user"):
            del public_apps[i]
        i += 1
    
    del i
    app = input("Enter the name of the app you want to run, or enter 'help' to see a list of apps.\n>")
    if app == "help":
        for a in os.listdir(f"apps/user/{json_data['CURRENT']['username']}") + public_apps:
            print(a)
        return home(True)
    elif app == "":
        return home()
    elif app in os.listdir(f"apps/user/{json_data['CURRENT']['username']}") + public_apps:
        return apps.run(app)
    else:
        print("Invalid app.")
        return run_app(True)


def delete_account():
    utils.clear_console()
    confirmation = hashlib.sha256(input("Enter your password to confirm.\n>").encode("utf-8")).hexdigest()
    if confirmation == json_data["CURRENT"]["password"]:
        for i in range(len(json_data["ACCOUNTS"])):
            if json_data["ACCOUNTS"][i] == json_data["CURRENT"]:
                del json_data["ACCOUNTS"][i]
                save()
                break
        shutil.rmtree(f"apps/user/{json_data['CURRENT']['username']}")
        json_data["CURRENT"] = None
        save()
        from system import account
        account.update()
        account.login()
    else:
        print("Incorrect password.")
        home(True)


def install_app():
    utils.clear_console()
    confirmation = hashlib.sha256(input("Enter your password to confirm.\n>").encode("utf-8")).hexdigest()
    if confirmation == json_data["CURRENT"]["password"]:
        app = input("Enter the app you want to get.\n>")
        for a in os.listdir("extensions"):
            if a in ("__init__.py", "__pycache__"):
                continue
            else:
                if app == a:
                    break
        else:
            print("Invalid app.")
            home(True)
        if os.path.exists(f"apps/{app}") or os.path.exists(f"apps/user/{json_data['CURRENT']['username']}/{app}"):
            print("App already exists.")
            home(True)
        if json_data["CURRENT"]["has_admin"]:
            public = utils.y_n("Do you want to publicly install this app?")
            if public:
                shutil.copytree(f"extensions/{app}", f"apps/{app}")
            else:
                shutil.copytree(f"extensions/{app}", f"apps/user/{json_data['CURRENT']['username']}/{app}")
        else:
            shutil.copytree(f"extensions/{app}", f"apps/user/{json_data['CURRENT']['username']}/{app}")
        
    else:
        print("Incorrect password.")
        home(True)


def delete_all_accounts():
    global json_data
    utils.clear_console()
    confirmation = hashlib.sha256(input("Enter your password to confirm.\n>").encode("utf-8")).hexdigest()
    if confirmation == json_data["CURRENT"]["password"]:
        for a in json_data["ACCOUNTS"]:
            shutil.rmtree(f"apps/user/{a['username']}")
        json_data = {"CURRENT": None, "ACCOUNTS": []}
        save()
        from system import account
        account.login()
    else:
        print("Incorrect password.")
        home(True)


def logout():
    json_data["CURRENT"] = None
    save()
    from system import account
    account.login()
