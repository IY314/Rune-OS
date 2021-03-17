import json, sys, hashlib, os
sys.path.append("../")
from system import homepage, utils

selected_account = None
json_data = {}

DEBUG = True
DEFAULT_JSON_DATA = {"CURRENT": None, "ACCOUNTS": []}


def update():
    global json_data
    try:
        with open("system/info.json") as f:
            json_data = json.loads(f.read())
    except FileNotFoundError:
        with open("system/info.json", "w+") as f:
            f.write(json.dumps(DEFAULT_JSON_DATA))
            json_data = DEFAULT_JSON_DATA

    del f


update()


def save():
    with open("system/info.json", "w") as f:
        f.write(json.dumps(json_data))
    del f


class Account:
    params = (
        "username",
        "password",
        "has_admin"
    )
    accounts = []

    def __init__(self, **kw):
        if kw:
            for k in kw:
                if k not in self.params:
                    raise TypeError(f"Expected valid parameter, received '{k}'.")
                setattr(self, k, kw[k])
            try:
                utils.dummy(
                    self.username,
                    self.password,
                    self.has_admin
                )
            except AttributeError:
                raise TypeError("Expected a value for username, password, and has_admin.")
        else:
            self.get_info()
        self.dict = {
            "username": self.username,
            "password": self.password,
            "has_admin": self.has_admin
        }
        json_data["ACCOUNTS"].append(self.dict)
        os.makedirs(f"apps/user/{self.username}")
        with open(f"apps/user/{self.username}/__init__.py", "w+"):
            pass
        save()

    def get_info(self):
        while True:
            possible_username = utils.ask("Enter a username.")
            for user in json_data["ACCOUNTS"]:
                if possible_username == user["username"]:
                    print("That username is taken.")
                    break
            else:
                self.username = possible_username
                break
        self.password = hashlib.sha256(utils.ask("Enter a secure password.", confirm=2,
            confirm_response="Type it again.", min_letters=8).encode("utf-8")).hexdigest()
        self.has_admin = True if json_data["ACCOUNTS"] == [] else False
    

def login():
    global selected_account
    utils.clear_console()
    prompt1 = "Enter 1 to create a new account."
    try:
        if json_data["ACCOUNTS"] == []:
            pass
        else:
            prompt1 += "\nEnter 2 to login to an existing account."
        prompt1 += "\nEnter anything else to shut down."
    except KeyError:
        json_data["ACCOUNTS"] = []
    
    account_choice = input(prompt1 + "\n>")
    if account_choice == "1":
        utils.clear_console()
        new_account = Account()
        utils.dummy(new_account)
        json_data["CURRENT"] = new_account.dict
        save()
        homepage.launch()
    elif account_choice == "2" and json_data["ACCOUNTS"] != []:
        update()
        return match_account()
    elif account_choice == "ENTER_TEST_MODE":
        encrypted_pass = hashlib.sha256(b"1234").hexdigest()
        test_account = Account(username="test-1", password=encrypted_pass, has_admin=True)
        utils.dummy(test_account)
        selected_account = test_account.dict
        json_data["CURRENT"] = selected_account
        save()
        return homepage.launch()
    else:
        exit()


def match_account(noclear=False):
    global selected_account
    if not noclear: utils.clear_console()
    existing_choice = input("Enter the username and password of that account.\nLeave blank to go back.\nUsername: ")
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
        return match_account(True)
    if code == "PASS":
        return match_password()
    elif code == "CLEAR":
        return login()


def match_password(noclear=False):
    global selected_account
    if not noclear: utils.clear_console()
    password_choice = input("Password: ")
    hashed = hashlib.sha256(password_choice.encode("utf-8")).hexdigest()
    if password_choice == "":
        return match_account()
    elif hashed != selected_account["password"]:
        print("Incorrect password.")
        return match_password(True)
    else:
        json_data["CURRENT"] = selected_account
        save()
        return homepage.launch()
