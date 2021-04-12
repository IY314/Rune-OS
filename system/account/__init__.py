import json, sys, hashlib, os, getpass
sys.path.append("../")
from system import homepage, utils

json_data = {}

DEFAULT_JSON_DATA = {"CURRENT": None, "ACCOUNTS": []}


def update():
    global json_data
    try:
        with open(utils.universal_path("system/info.json")) as f:
            json_data = json.loads(f.read())
    except FileNotFoundError:
        with open(utils.universal_path("system/info.json"), "w+") as f:
            f.write(json.dumps(DEFAULT_JSON_DATA))
            json_data = DEFAULT_JSON_DATA

    del f


update()


def save():
    with open(utils.universal_path("system/info.json"), "w") as f:
        f.write(json.dumps(json_data))
    del f


class Account:
    accounts = []

    def __init__(self, *, username=None, password=None, has_admin=None):
        if any((username, password, has_admin)):
            if not username:
                self.get_info("username")
            else:
                self.username = username

            if not password:
                self.get_info("password")
            else:
                self.password = password

            if has_admin == None:
                self.get_info("has_admin")
            else:
                self.has_admin = has_admin

        else:
            self.get_info()
        self.dict = {
            "username": self.username,
            "password": self.password,
            "has_admin": self.has_admin
        }
        json_data["ACCOUNTS"].append(self.dict)
        os.makedirs(utils.universal_path(f"apps/user/{self.username}"))
        with open(utils.universal_path(f"apps/user/{self.username}/__init__.py"), "w+"):
            pass
        save()

    def get_info(self, field=None):
        def username():
            while True:
                possible_username = utils.ask("Enter a username.")
                for user in json_data["ACCOUNTS"]:
                    if possible_username == user["username"]:
                        print("That username is taken.")
                        break
                else:
                    self.username = possible_username
                    break

        def password():
            self.password = hashlib.sha256(utils.ask("Enter a secure password.", confirm=2,
                confirm_response="Type it again.", min_letters=8).encode("utf-8")).hexdigest()

        def has_admin():
            self.has_admin = True if json_data["ACCOUNTS"] == [] else False

        if field:
            if field == "username":
                username()
            elif field == "password":
                password()
            elif field == "has_admin":
                has_admin()
            else:
                raise TypeError("Invalid field")
        else:
            username()
            password()
            has_admin()


def login(clear=True):
    def create_account():
        utils.clear_console()
        new_account = Account()
        dummy(new_account)
        json_data["CURRENT"] = new_account.dict
        save()
        return homepage.launch()

    def login_account():
        update()
        return match_account()

    if clear: utils.clear_console()

    if json_data["ACCOUNTS"] == []:
        utils.make_choice_box("Login",
            ("create a new account", create_account),
            anything_else=("shut down", exit), form="left"
        )
    else:
        utils.make_choice_box("Login",
            ("create a new account", create_account),
            ("login to an existing account", login_account),
            anything_else=("shut down", exit), form="left"
        )


def match_account(clear=True):
    if clear: utils.clear_console()
    existing_choice = input("Username: ")
    for a in json_data["ACCOUNTS"]:
        if existing_choice == "":
            code = "CLEAR"
            break
        if existing_choice == a["username"]:
            selected_account = a
            code = "PASS"
            break
    else:
        print("Invalid account.")
        return match_account(False)
    if code == "PASS":
        return match_password(selected_account, False)
    elif code == "CLEAR":
        return login()


def match_password(selected_account, clear=True):
    if clear: utils.clear_console()
    password_choice = getpass.getpass("Password: ")
    hashed = hashlib.sha256(password_choice.encode("utf-8")).hexdigest()
    if password_choice == "":
        return match_account()
    elif hashed != selected_account["password"]:
        print("Incorrect password.")
        return match_password(selected_account, False)
    else:
        json_data["CURRENT"] = selected_account
        save()
        return homepage.launch()
