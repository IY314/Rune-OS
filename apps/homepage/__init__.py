import json, time, os, sys # , hashlib
sys.path.append("../")
import apps
from apps import utils

json_data = {}


def update():
    global json_data
    with open("info.json") as f:
        json_data = json.loads(f.read())

    del f


def save():
    with open("info.json", "w") as f:
        f.write(json.dumps(json_data))


def launch():
    now = int(time.strftime("%H"))
    if now <= 4 or now > 22:
        tod = "night"
    elif now > 16 and now <= 22:
        tod = "evening"
    elif now > 12 and now <= 16:
        tod = "afternoon"
    elif now > 5 and now <= 12:
        tod = "morning"
    update()
    user = json_data["CURRENT"]["username"]
    print(f"Good {tod}, {user}!")
    while True:
        home()


def home():
    global json_data
    options = "Enter 1 to run an app."
    if json_data["CURRENT"]["has_admin"]:
        options += "\nEnter 2 to clear all accounts."
    options += "\nEnter anything else to logout."
    print(options)
    action = input(">")
    if action == "1":
        run_app()
    elif action == "2" and json_data["CURRENT"]["has_admin"]:
        confirmation = utils.y_n("This will clear all accounts, including yours. Are you sure?")
        if confirmation:
            json_data = {"CURRENT": None, "ACCOUNTS": []}
            save()
            from apps import account
            account.login()
        """
    elif action == "3" and json_data["CURRENT"]["has_admin"]:
        account_choice = input("Account Username: ")
        for a in json_data["ACCOUNTS"]:
            if a["username"] == account_choice:
                password_check = input("Admin Password: ")
                hashed = hashlib.sha256(password_check.encode("utf-8")).hexdigest()
                if hashed == json_data["CURRENT"]["password"]:
                    print(a["password"])
                else:
                    print("Incorrect password, access denied.")
                break
        else:
            print("Invalid account.")
        home()
        """
    else:
        json_data["CURRENT"] = None
        save()
        from apps import account
        account.login()


def run_app():
    while True:
        app = input("Enter the name of the app you want to run, or enter 'help' to see a list of apps.\n>")
        if app == "help":
            for a in os.listdir("apps"):
                if a in ("__pycache__", "__init__.py", "homepage", "utils", "account"):
                    continue
                else:
                    print(a)
            return home()
        for a in os.listdir("apps"):
            if a in ("__pycache__", "__init__.py", "homepage", "utils", "account"):
                continue
            else:
                if app == a:
                    return apps.run(app)
        print("Invalid app.")
