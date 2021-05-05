import sys
import os
import shutil

import time
import getpass
import hashlib

sys.path.append("../")

import apps
import installation

from system import utils

data = utils.File("system/accounts.json")
data.update()

public_path = utils.Path("apps/public")
private_path = utils.Path(f"apps/private/{data.data['CURRENT']['username']}")


def check_password(clear=True):
    def decorator(func):
        def wrapper(*args, **kw):
            if clear: utils.clear_console()
            print(utils.make_box("Enter your password to confirm.", title=False))
            confirmation = hashlib.sha256(getpass.getpass(">").encode("utf-8")).hexdigest()
            if confirmation == data.data["CURRENT"]["password"]:
                return func(*args, **kw)
            else:
                print("Incorrect password.")
                return home()

        return wrapper
    return decorator


def launch():
    utils.clear_console()
    now = int(time.strftime("%H"))
    if now > 16 or now <= 1:
        tod = "evening"
    elif now > 12 and now <= 16:
        tod = "afternoon"
    elif now > 2 and now <= 12:
        tod = "morning"
    else:
        raise utils.ProgrammerError(f"The time is not handled ({now})!")
    data.update()
    user = data.data["CURRENT"]["username"]
    greeting = f"Good {tod}, {user}!"
    return home(greeting=greeting)


def home(clear=False, greeting="Home"):
    if clear: utils.clear_console()

    utils.make_choice_box(greeting,
        ("run an app", run_app),
        ("install an app", install_app),
        ("uninstall an app", uninstall_app),
        ("edit your account", edit_account),
        ("delete your account", delete_account),
        ("remotely create an account", create_account, True),
        ("change an account's access", change_access, True),
        ("clear all accounts", delete_all_accounts, True),
        anything_else=("logout", logout), condition=data.data["CURRENT"]["has_admin"], form="left"
    )


def run_app(clear=True):
    if clear: utils.clear_console()
    public_apps = os.listdir(public_path.path)
    private_apps = os.listdir(private_path.path)
    i = 0
    while i < len(public_apps):
        if public_apps[i] in ("__init__.py", "__pycache__"):
            del public_apps[i]
        i += 1
    i = 0
    while i < len(private_apps):
        if private_apps[i] in ("__init__.py", "__pycache__"):
            del private_apps[i]
        i += 1
    del i
    app = input(utils.make_box("Run App", "Enter the name of the app you want to run, or enter 'help' to see a list of apps.", form="left") + "\n>")
    if app == "help":
        for a in private_apps + public_apps:
            print(a)
        return home()
    elif app == "":
        return home(True)
    elif app in private_apps + public_apps:
        return apps.run(app)
    else:
        print("Invalid app.")
        return run_app(False)


@check_password(False)
def delete_account():
    for i in range(len(data.data["ACCOUNTS"])):
        if data.data["ACCOUNTS"][i] == data.data["CURRENT"]:
            del data.data["ACCOUNTS"][i]
            data.save()
            break
    shutil.rmtree(private_path.path)
    data.data["CURRENT"] = None
    data.save()
    from system import account
    account.data.update()
    return account.login()


def install_app():
    return app("Install")


def uninstall_app():
    return app("Uninstall")


@check_password()
def app(type_):
    app = input(utils.make_box(f"{type_} App", f"Enter the app you want to {type_.lower()}.", form="left") + "\n>")
    if app == "":
        return home(True)
    try:
        if type_ == "Install":
            path = public_path.copy()
            if data.data["CURRENT"]["has_admin"]:
                public = utils.y_n(utils.make_box("Do you want to publicly install this app?", title=False))
            if not public:
                path.update_path(private_path.path)
            installation.install(app, path.path)
            return home(True)
        elif type_ == "Uninstall":
            path = private_path.copy()
            location = installation.search(app, path)
            if location == "local":
                installation.uninstall(app, path)
                return home(True)
            else:
                if not data.data["CURRENT"]["has_admin"]:
                    print("Access denied.")
                    return home()
                installation.uninstall(app, public_path)
                return home(True)
    except Exception as err:
        print(err)
        return home()


@check_password()
def edit_account():
    def username():
        old = data.data["CURRENT"]["username"]
        new = utils.ask("Enter the new username.", confirm=1, confirm_response="Are you sure?")
        data.data["CURRENT"]["username"] = new
        for a in range(len(data.data["ACCOUNTS"])):
            if data.data["ACCOUNTS"][a]["password"] == data.data["CURRENT"]["password"]:
                data.data["ACCOUNTS"][a]["username"] = new
                data.save()
        private_path.update_path(f"apps/private/{new}")
        os.rename(utils.Path().universal_path(f"apps/private/{old}"), utils.Path().universal_path(f"apps/private/{new}"))

    def password():
        old = getpass.getpass("Enter the old password.\n>")
        if data.data["CURRENT"]["password"] == hashlib.sha256(old.encode("utf-8")).hexdigest():
            new = hashlib.sha256(utils.ask("Enter the new password.", confirm=2, confirm_response="Type it again.", min_letters=8).encode("utf-8")).hexdigest()
            data.data["CURRENT"]["password"] = new
            for a in range(len(data.data["ACCOUNTS"])):
                if data.data["ACCOUNTS"][a]["username"] == data.data["CURRENT"]["username"]:
                    data.data["ACCOUNTS"][a]["password"] = new
                    data.save()

    utils.make_choice_box("Edit Account",
        ("edit your username", username),
        ("edit your password", password),
        anything_else=("return home", lambda: home(True)), condition=True, form="left"
    )
    return home(True)


@check_password()
def delete_all_accounts():
    for a in data.data["ACCOUNTS"]:
        shutil.rmtree(utils.Path().universal_path(f"apps/private/{a['username']}"))
    data.data = {"CURRENT": None, "ACCOUNTS": []}
    data.save()
    from system import account
    account.data.update()
    return account.login()


@check_password()
def create_account():
    has_admin = utils.y_n(utils.make_box("Do you want this account to have admin powers?"))
    from system import account
    utils.clear_console()
    new_account = account.Account(has_admin=has_admin)
    utils.dummy(new_account)
    data.data["CURRENT"] = new_account.dict
    data.save()
    return launch()


@check_password()
def change_access():

    action = None

    def promote():
        nonlocal action
        action = "promote"

    def demote():
        nonlocal action
        action = "demote"

    utils.make_choice_box("Change Access",
        ("promote an account", promote),
        ("demote an account", demote),
        anything_else=("return home", lambda: home(True)), condition=True, form="left"
    )

    user = input(utils.make_box("Which user do you want to promote?", title=False) + "\n>")
    for u in data.data["ACCOUNTS"]:
        if u["username"] == user:
            user = u
            break
    else:
        print("Invalid user.")
        return home()
    if user["has_admin"] and action == "promote":
        print("That user already has admin access.")
        return home()
    if not user["has_admin"] and action == "demote":
        print("That user does not have admin access.")
        return home()
    user["has_admin"] = not user["has_admin"]
    data.save()
    return home(True)


def logout():
    data.data["CURRENT"] = None
    data.save()
    from system import account
    return account.login()
