import os
import time
import sys

import getpass
import builtins
import re
import _io
import json

DEFAULT_DELAYS = {
    r'\n': 0.5,
    r'\s': 0.3,
    r'\w': 0.1
}


class ProgrammerError(Exception):
    pass


def ask(question, *, confirm=0, confirm_response=None, accepted_responses=None, error_message='Invalid answer.', min_letters=4):
    if any((confirm, confirm_response)) and not all((confirm, confirm_response)):
        if not confirm_response:
            raise TypeError(f'Argument confirm is {str(confirm)}, but there is no value set for confirm_response!')
        else:
            raise TypeError('Argument confirm is 0, but there is a value set for confirm_response!')
    clear_console()
    while True:
        if confirm == 2:
            input = getpass.getpass
        else:
            input = builtins.input
        ans = input(question + '\n>')
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
            ans2 = input(confirm_response + '\n>')
            if ans2 != ans:
                print('They do not match!')
                continue
        return ans


def y_n(message, *, error_message='Invalid answer.', yes=('y', 'yes', 'aye', 'yea'),  no=('n', 'no', 'nope')):
    clear_console()
    while True:
        ans = input(message + '\n>')
        if ans.lower() in yes:
            return True
        elif ans.lower() in no:
            return False
        else:
            clear_console()
            print(error_message)


class Path:
    def __init__(self, path=None):
        if path:
            self.path = self.universal_path(path)

    def universal_path(self, path=None):
        if not path:
            path = self.path
        return os.path.join(*path.split('/'))

    def import_path(self, path=None):
        if not path:
            path = self.path
        return '.'.join(path.split(os.path.sep))

    def update_path(self, path):
        self.path = self.universal_path(path)

    def copy(self):
        return Path(self.path)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def make_box(*strs, chars=None, form='centered', title=True):
    return_str = []
    strs = list(strs)
    if not chars:
        record = len(strs[0])
        for s in range(len(strs)):
            if is_even(len(strs[s])):
                strs[s] += ' '
            if len(strs[s]) > record:
                record = len(strs[s])
        chars = record
    if not title:
        strs.insert(0, '\\start\\')
    if strs[-1] != '\\end\\':
        strs.append('\\end\\')
    for s in range(len(strs)):
        text = strs[s]
        length = len(text)
        num = int((chars - length) / 2) if form == 'centered' else chars - length
        fillchar = '-' if s == 0 or strs[s] == strs[-1] else ' '
        endchar = '+' if s == 0 or strs[s] == strs[-1] else '|'
        if text in ('\\end\\', '\\start\\'):
            return_str.append(endchar + (chars + 2) * fillchar + endchar)
        else:
            if form == 'left':
                line = endchar + ' ' + text + ' ' + num * fillchar + endchar
            elif form == 'centered':
                line = endchar + num * fillchar + ' ' + text + ' ' + num * fillchar + endchar
            elif form == 'right':
                line = endchar + num * fillchar + ' ' + text + ' ' + endchar
            return_str.append(line)
    return '\n'.join(return_str)


def make_choice_box(header=None, *options, anything_else, condition=True, **box_options):
    data = File('system/accounts.json')

    choices = []
    title = False
    if header:
        choices.append(header)
        title = True
    for o in range(len(options)):
        try:
            data.update()
            if options[o][2]:
                if condition:
                    raise IndexError()
            else:
                continue
        except IndexError:
            choices.append(f'Enter {str(o + 1)} to {options[o][0]}.')
    choices.append(f'Enter anything else to {anything_else[0]}.')
    print(make_box(*choices, **box_options, title=title))
    i = input('>')
    try:
        int_i = int(i)
        try:
            return options[int_i - 1][1]()
        except IndexError:
            raise ValueError()
    except ValueError:
        return anything_else[1]()


def tprint(*vals, sep=' ', end='\n', file=sys.stdout, delays=DEFAULT_DELAYS):
    if type(file) == _io.TextIOWrapper:
        print(*vals, sep=sep, end=end, file=file)
        return
    string = sep.join([str(val) for val in vals]) + end
    try:
        dummy(
            delays[r'\n'],
            delays[r'\s'],
            delays[r'\w']
        )
    except KeyError:
        raise TypeError('Parameter `delays` must have at least three values: \'\\n\', \'\\s\', and \'\\w\'.')
    for char in string:
        print(char, file=file, flush=True)
        for k in delays:
            if re.compile(k, re.VERBOSE).search(char):
                delay = delays[k]
        time.sleep(delay)


def conceal(string, *, letters_shown=4, letter='*'):
    return f'{letter * (len(string) - letters_shown) + string[(-1 * letters_shown):]}'


def repeat(times):
    def decorator(func):
        def wrapper(*args, **kw):
            for _ in range(times):
                func(*args, **kw)

        return wrapper

    return decorator


def dummy(*args, **kw):
    pass


def is_even(num):
    raw = num / 2
    as_int = int(num / 2)
    if as_int == raw:
        return True
    else:
        return False


class File:
    def __init__(self, filename):
        self.filename = Path(filename)
        self.data = None
        self.update()

    def save(self):
        with open(self.filename.path, 'w') as f:
            f.write(json.dumps(self.data))

    def update(self):
        with open(self.filename.path) as f:
            self.data = json.loads(f.read())

