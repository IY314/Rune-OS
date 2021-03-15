import json, sys
sys.path.append("../")
from apps import utils
from apps import homepage

selected_account = None

DEBUG = True
DEFAULT_JSON_DATA = {"CURRENT": None, "ACCOUNTS": []}

try:
    with open("info.json") as f:
        json_data = json.loads(f.read())
except FileNotFoundError:
    with open("info.json", "w+") as f:
        f.write(json.dumps(DEFAULT_JSON_DATA))
        json_data = DEFAULT_JSON_DATA

del f


def save():
    with open("info.json", "w") as f:
        f.write(json.dumps(json_data))


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
        self.accounts.append({
            "username": self.username,
            "password": self.password,
            "has_admin": self.has_admin
        })
        json_data["ACCOUNTS"] = self.accounts
        save()
    
    def __repr__(self):
        return f"""
        USERNAME: {self.username}
        PASSWORD: {utils.conceal(self.password)}
        """

    def get_info(self):
        self.username  = utils.ask("Enter a username.")
        self.password  = utils.ask("Enter a secure password.", confirm=2, confirm_response="Type it again.", min_letters=8)
        self.has_admin = False
    

def login():
    global selected_account
    while True:
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
            new_account = Account()
            utils.dummy(new_account)
        elif account_choice == "2":
            if json_data["ACCOUNTS"] == []:
                return match_account()
            else:
                exit()
        elif account_choice == "ENTER_TEST_MODE":
            test_account = Account(username="test-1", password="1234", has_admin=True)
            utils.dummy(test_account)
            selected_account = {
                "username": "test-1",
                "password": "1234",
                "has_admin": True
            }
            json_data["CURRENT"] = selected_account
            save()
            return homepage.launch()
        else:
            exit()


def match_account():
    global selected_account
    while True:
        existing_choice = input("Enter the username and password of that account.\nLeave blank to go back.\nUsername: ")
        if existing_choice == "":
            return login()
        for a in json_data["ACCOUNTS"]:
            if existing_choice == a["username"]:
                selected_account = a
                return match_password()
        print("Invalid account.")
        continue


def match_password():
    global selected_account
    while True:
        password_choice = input("Password: ")
        if password_choice == "":
            return match_account()
        elif password_choice != selected_account["password"]:
            print("Incorrect password.\nPassword: ")
            continue
        else:
            json_data["CURRENT"] = selected_account
            save()
            return homepage.launch()


if __name__ == "__main__":
    login()
