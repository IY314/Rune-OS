import json, time, os, sys, hashlib, shutil
sys.path.append("../")
import apps, installation
from system import utils

json_data = {}


def update():
    global json_data
    with open(utils.universal_path("system/info.json")) as f:
        json_data = json.loads(f.read())

    del f


def save():
    with open(utils.universal_path("system/info.json"), "w") as f:
        f.write(json.dumps(json_data))


def check_password():
    global json_data
    confirmation = hashlib.sha256(input("Enter your password to confirm.\n>").encode("utf-8")).hexdigest()
    return confirmation == json_data["CURRENT"]["password"]


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
    home()


def home(clear=False):
    global json_data
    if clear: utils.clear_console()
    options = "Enter 1 to run an app.\nEnter 2 to delete your account.\nEnter 3 to install an app.\nEnter 4 to uninstall an app."
    if json_data["CURRENT"]["has_admin"]:
        options += "\nEnter 5 to clear all accounts.\nEnter 6 to remotely create an account.\nEnter 7 to promote or demote an account's admin access."
    options += "\nEnter anything else to logout."
    print(options)
    action = input(">")
    if action == "1":
        run_app()
    elif action == "2":
        delete_account()
    elif action == "3":
        install_app()
    elif action == "4":
        uninstall_app()
    elif action == "5" and json_data["CURRENT"]["has_admin"]:
        delete_all_accounts()
    elif action == "6" and json_data["CURRENT"]["has_admin"]:
        create_account()
    elif action == "7" and json_data["CURRENT"]["has_admin"]:
        change_access()
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
        for a in os.listdir(utils.universal_path(f"apps/user/{json_data['CURRENT']['username']}")) + public_apps:
            print(a)
        return home()
    elif app == "":
        return home(True)
    elif app in os.listdir(utils.universal_path(f"apps/user/{json_data['CURRENT']['username']}")) + public_apps:
        return apps.run(app)
    else:
        print("Invalid app.")
        return run_app(True)


def delete_account():
    utils.clear_console()
    if check_password():
        for i in range(len(json_data["ACCOUNTS"])):
            if json_data["ACCOUNTS"][i] == json_data["CURRENT"]:
                del json_data["ACCOUNTS"][i]
                save()
                break
        shutil.rmtree(utils.universal_path(f"apps/user/{json_data['CURRENT']['username']}"))
        json_data["CURRENT"] = None
        save()
        from system import account
        account.update()
        account.login()
    else:
        print("Incorrect password.")
        home()


def install_app():
    utils.clear_console()
    if check_password():
        app = input("Enter the app you want to get.\n>")
        path = "apps"
        if json_data["CURRENT"]["has_admin"]:
            public = utils.y_n("Do you want to publicly install this app?")
            if not public:
                path = utils.universal_path(f"apps/user/{json_data['CURRENT']['username']}")
        try:
            installation.install(app, path)
            home()
        except ModuleNotFoundError as err:
            print(err)
            home()
    else:
        print("Incorrect password.")
        home()


def uninstall_app():
    utils.clear_console()
    if check_password():
        app = input("Enter the app you want to uninstall.\n>")
        try:
            path = utils.universal_path(f"apps/user/{json_data['CURRENT']['username']}")
            location = installation.search(app, path)
            if location == "local":
                installation.uninstall(app, path)
            else:
                if not json_data["CURRENT"]["has_admin"]:
                    print("Access denied.")
                    home()
                installation.uninstall(app, "apps")
                home()
        except ModuleNotFoundError as err:
            print(err)
            home()
    else:
        print("Incorrect password.")
        home()


def delete_all_accounts():
    global json_data
    utils.clear_console()
    if check_password():
        for a in json_data["ACCOUNTS"]:
            shutil.rmtree(utils.universal_path(f"apps/user/{a['username']}"))
        json_data = {"CURRENT": None, "ACCOUNTS": []}
        save()
        from system import account
        account.login()
    else:
        print("Incorrect password.")
        home()


def create_account():
    utils.clear_console()
    if check_password():
        has_admin = utils.y_n("Do you want this account to have admin powers?\n>")
        from system import account
        utils.clear_console()
        new_account = account.Account(has_admin=has_admin)
        utils.dummy(new_account)
        json_data["CURRENT"] = new_account.dict
        save()
        launch()


def change_access():
    utils.clear_console()
    if check_password():
        print("Enter 1 to promote an account.\nEnter 2 to demote an account.\nEnter anything else to return home.")
        level = input(">")
        if level == "1":
            user = input("Which user do you want to promote?\n>")
            for u in json_data["ACCOUNTS"]:
                if u["username"] == user:
                    user = u
                    break
            else:
                print("Invalid user.")
                return home()
            if user["has_admin"]:
                print("That user already has admin access.")
                return home()
            user["has_admin"] = True
            save()
            return home(True)
        elif level == "2":
            user = input("Which user do you want to demote?\n>")
            for u in json_data["ACCOUNTS"]:
                if u["username"] == user:
                    user = u
                    break
            else:
                print("Invalid user.")
                return home()
            if not user["has_admin"]:
                print("That user does not have admin access.")
                return home()
            user["has_admin"] = False
            save()
            return home(True)
        else:
            home(True)


def logout():
    json_data["CURRENT"] = None
    save()
    from system import account
    account.login()
