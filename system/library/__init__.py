import re, time, sys
from system import utils

DEFAULT_DELAYS = {
    r"\n": 0.5,
    r"\s": 0.3,
    r"\w": 0.1
}


def tprint(*vals, sep=" ", end="\n", file=sys.stdout, delays=DEFAULT_DELAYS):
    string = sep.join([str(val) for val in vals]) + end
    try:
        utils.dummy(
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


def conceal(string, *, letters_shown=4, letter="*"):
    return f"{letter * (len(string) - letters_shown) + string[(-1 * letters_shown):]}"


def repeat(times):
    def decorator(func):
        def wrapper(*args, **kw):
            for _ in range(times):
                func(*args, **kw)
        
        return wrapper
    
    return decorator
