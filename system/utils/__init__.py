ALL = None


def dummy(*args, **kw):
    pass


def ask(question, *, confirm=0, confirm_response=None, accepted_responses=ALL, error_message="Invalid answer.", min_letters=4):
    """Asks a question specified by the user."""
    if confirm:
        if not confirm_response:
            raise TypeError("Argument confirm is True, but there is no value set for confirm_response!")
    while True:
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
