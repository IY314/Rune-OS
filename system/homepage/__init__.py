import json, time, os, sys, hashlib, shutil, getpass
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
    print(utils.make_box("Enter your password to confirm.", title=False))
    confirmation = hashlib.sha256(getpass.getpass(">").encode("utf-8")).hexdigest()
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
    greeting = f"Good {tod}, {user}!"
    return home(greeting=greeting)


def home(clear=False, greeting="Home"):
    global json_data
    if clear: utils.clear_console()

    if json_data["CURRENT"]["has_admin"]:
        utils.make_choice_box(greeting,
            ("run an app", run_app),
            ("install an app", install_app),
            ("uninstall an app", uninstall_app),
            ("edit your account", edit_account),
            ("delete your account", delete_account),
            ("remotely create an account", create_account),
            ("change an account's access", change_access),
            ("clear all accounts", delete_all_accounts),
            anything_else=("logout", logout), form="left"
        )
    else:
        utils.make_choice_box(greeting,
            ("run an app", run_app),
            ("install an app", install_app),
            ("uninstall an app", uninstall_app),
            ("edit your account", edit_account),
            ("delete your account", delete_account),
            anything_else=("logout", logout), form="left"
        )


def run_app(clear=True):
    if clear: utils.clear_console()
    public_apps = os.listdir(utils.universal_path("apps/public"))
    i = 0
    while i < len(public_apps):
        if public_apps[i] in ("__init__.py", "__pycache__"):
            del public_apps[i]
        i += 1

    del i
    app = input(utils.make_box("Run App", "Enter the name of the app you want to run, or enter 'help' to see a list of apps.", form="left") + "\n>")
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
        return run_app(False)


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
        return account.login()
    else:
        print("Incorrect password.")
        return home()


def install_app():
    utils.clear_console()
    if check_password():
        app = input(utils.make_box("Install App", "Enter the app you want to get.", form="left") + "\n>")
        path = utils.universal_path("apps/public")
        if json_data["CURRENT"]["has_admin"]:
            public = utils.y_n(utils.make_box("Do you want to publicly install this app?", title=False))
            if not public:
                path = utils.universal_path(f"apps/user/{json_data['CURRENT']['username']}")
        try:
            installation.install(app, path)
            return home(True)
        except ModuleNotFoundError as err:
            print(err)
            return home()
    else:
        print("Incorrect password.")
        return home()


def uninstall_app():
    utils.clear_console()
    if check_password():
        app = input(utils.make_box("Uninstall App", "Enter the app you want to uninstall.", form="left") + "\n>")
        try:
            path = utils.universal_path(f"apps/user/{json_data['CURRENT']['username']}")
            location = installation.search(app, path)
            if location == "local":
                installation.uninstall(app, path)
            else:
                if not json_data["CURRENT"]["has_admin"]:
                    print("Access denied.")
                    return home()
                installation.uninstall(app, utils.universal_path("apps/public"))
                return home(True)
        except Exception as err:
            print(err)
            return home()
    else:
        print("Incorrect password.")
        return home()


def edit_account():
    def username():
        old = json_data["CURRENT"]["username"]
        new = utils.ask("Enter the new username.", confirm=1, confirm_response="Are you sure?")
        json_data["CURRENT"]["username"] = new
        for a in range(len(json_data["ACCOUNTS"])):
            if json_data["ACCOUNTS"][a]["password"] == json_data["CURRENT"]["password"]:
                json_data["ACCOUNTS"][a]["username"] = new
                save()
        os.rename(utils.universal_path(f"apps/user/{old}"), utils.universal_path(f"apps/user/{new}"))

    def password():
        old = utils.ask("Enter the old password.")
        if json_data["CURRENT"]["password"] == hashlib.sha256(old.encode("utf-8")).hexdigest():
            new = hashlib.sha256(utils.ask("Enter the new password.", confirm=2, confirm_response="Type it again.", min_letters=8).encode("utf-8")).hexdigest()
            json_data["CURRENT"]["password"] = new
            for a in range(len(json_data["ACCOUNTS"])):
                if json_data["ACCOUNTS"][a]["username"] == json_data["CURRENT"]["username"]:
                    json_data["ACCOUNTS"][a]["password"] = new
                    save()

    utils.clear_console()

    if check_password():
        utils.make_choice_box("Edit Account",
            ("edit your username", username),
            ("edit your password", password),
            anything_else=("return home", lambda: home(True)), form="left"
        )
        return home(True)
    else:
        print("Incorrect password.")
        return home()


def delete_all_accounts():
    global json_data
    utils.clear_console()
    if check_password():
        for a in json_data["ACCOUNTS"]:
            shutil.rmtree(utils.universal_path(f"apps/user/{a['username']}"))
        json_data = {"CURRENT": None, "ACCOUNTS": []}
        save()
        from system import account
        return account.login()
    else:
        print("Incorrect password.")
        return home()


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
        return launch()


def change_access():
    def promote():
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

    def demote():
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

    utils.clear_console()
    if check_password():
        utils.make_choice_box("Change Access",
            ("promote an account", promote),
            ("demote an account", demote),
            anything_else=("return home", lambda: home(True)), form="left"
        )
    else:
        print("Incorrect password.")
        return home()


def logout():
    json_data["CURRENT"] = None
    save()
    from system import account
    return account.login()
