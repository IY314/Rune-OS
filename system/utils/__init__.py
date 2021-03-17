import os, time, sys, re

ALL = None
DEFAULT_DELAYS = {
    r"\n": 0.5,
    r"\s": 0.3,
    r"\w": 0.1
}


def dummy(*args, **kw):
    pass


def tprint(*vals, sep=" ", end="\n", file=sys.stdout, delays=DEFAULT_DELAYS):
    string = sep.join([str(val) for val in vals]) + end
    try:
        dummy(
            delays[r"\n"],
            delays[r"\s"],
            delays[r"\w"]
        )
    except KeyError:
        raise TypeError("Parameter `delays` must have at least three values: '\\n', '\\s', and '\\w'.")
    for char in string:
        file.write(char)
        file.flush()
        for k in delays:
            if re.compile(k, re.VERBOSE).search(char):
                delay = delays[k]
        time.sleep(delay)


def ask(question, *, confirm=0, confirm_response=None, accepted_responses=ALL, error_message="Invalid answer.", min_letters=4):
    """Asks a question specified by the user."""
    if confirm:
        if not confirm_response:
            raise TypeError("Argument confirm is True, but there is no value set for confirm_response!")
    while True:
        clear_console()
        ans = input(question + "\n>")
        if accepted_responses:
            if ans not in accepted_responses:
                print(error_message)
                continue
        if len(ans) < min_letters:
            print(error_message)
            continue
        if confirm == 1:
            if y_n(confirm_response, error_message):
                return ans
            else:
                continue
        elif confirm == 2:
            ans2 = input(confirm_response + "\n>")
            if ans2 != ans:
                print("They do not match!")
                continue
        return ans


def y_n(message, error_message="Invalid answer."):
    while True:
        clear_console()
        ans = input(message + "\n>")
        if ans.lower() in ("y", "yes", "aye", "yea"):
            return True
        elif ans.lower() not in ("n", "no", "nope"):
            print(error_message)
            continue
        else:
            return False


def conceal(string, *, letters_shown=4, letter="*"):
    return f"{letter * (len(string) - letters_shown) + string[(-1 * letters_shown):]}"


def clear_console():
    os.system("clear")
