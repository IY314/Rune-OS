import os, time, sys, getpass, builtins
from system import library


def ask(question, *, confirm=0, confirm_response=None, accepted_responses=None, error_message="Invalid answer.", min_letters=4):
    """Asks a question specified by the user."""
    if confirm:
        if not confirm_response:
            raise TypeError("Argument confirm is True, but there is no value set for confirm_response!")
    while True:
        clear_console()
        if confirm == 2:
            input = getpass.getpass
        else:
            input = builtins.input
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


def make_box(*strs, chars=None, form="centered", title=True):
    return_str = []
    strs = list(strs)
    if not chars:
        record = len(strs[0])
        for s in range(len(strs)):
            if library.is_even(len(strs[s])):
                strs[s] += " "
            if len(strs[s]) > record:
                record = len(strs[s])
        chars = record
    if not title:
        strs.insert(0, "\\start\\")
    if strs[-1] != "\\end\\":
        strs.append("\\end\\")
    if form == "centered":
        for s in range(len(strs)):
            text = strs[s]
            length = len(text)
            num = int((chars - length) / 2)
            fillchar = "-" if s == 0 or strs[s] == strs[-1] else " "
            endchar = "+" if s == 0 or strs[s] == strs[-1] else "|"
            if text in ("\\end\\", "\\start\\"):
                return_str.append(endchar + (chars + 2) * fillchar + endchar)
            else:
                return_str.append(endchar + num * fillchar + " " + text + " " + num * fillchar + endchar)
    elif form in ("left", "right"):
        for s in range(len(strs)):
            text = strs[s]
            length = len(text)
            num = chars - length
            fillchar = "-" if s == 0 or strs[s] == strs[-1] else " "
            endchar = "+" if s == 0 or strs[s] == strs[-1] else "|"
            if text in ("\\end\\", "\\start\\"):
                return_str.append(endchar + (chars + 2) * fillchar + endchar)
            else:
                if form == "left":
                    line = endchar + " " + text + " " + num * fillchar + endchar
                else:
                    line = endchar + num * fillchar + " " + text + " " + endchar
                return_str.append(line)
    return "\n".join(return_str)
