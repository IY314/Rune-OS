import os, time, sys, getpass


def dummy(*args, **kw):
    pass


def ask(question, *, confirm=0, confirm_response=None, accepted_responses=None, error_message="Invalid answer.", min_letters=4):
    """Asks a question specified by the user."""
    if confirm:
        if not confirm_response:
            raise TypeError("Argument confirm is True, but there is no value set for confirm_response!")
    while True:
        clear_console()
        if confirm == 2:
            input = getpass.getpass
        ans = input(question + "\n>")
        if accepted_responses:
            if ans not in accepted_responses:
                print(error_message)
                continue
        if len(ans) < min_letters:
            print(error_message)
            continue
        if confirm == 1:
            if y_n(confirm_response, error_message=error_message):
                return ans
            else:
                continue
        elif confirm == 2:
            ans2 = input(confirm_response + "\n>")
            if ans2 != ans:
                print("They do not match!")
                continue
        return ans


def y_n(message, *, error_message="Invalid answer.", yes=("y", "yes", "aye", "yea"),  no=("n", "no", "nope")):
    """Translates user input into a boolean value (asks yes or no)"""
    while True:
        clear_console()
        ans = input(message + "\n>")
        if ans.lower() in yes:
            return True
        elif ans.lower() in no:
            return False
        else:
            print(error_message)


def universal_path(path: str):
    return os.path.join(*path.split("/"))


def clear_console():
    """Clears the console."""
    os.system("cls" if os.name == "nt" else "clear")
