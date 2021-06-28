# Building an App
WIP

Your app must be in the `installation` package/folder. If you put it in `public`, it will very likely be deleted and your app will be gone.

Apps are Python packages (the format is explained below).

Directory:
```
Rune OS
|
+-- apps
    |
    +-- private
        |
        +-- __init__.py
    |
    +-- public
        |
        +-- calc
            |
            +-- __init__.py
        |
        +-- __init__.py
    |
    +-- __init__.py
|
+-- installation
    |
    +-- GTN
        |
        +-- __init__.py
    |
    +-- tic_tac_toe
        |
        +-- __init__.py
    |
    +-- <app_name>
        |
        +-- __init__.py
        |
        +-- <other_files>
|
+-- system
    |
    +-- account
        |
        +-- __init__.py
    |
    +-- homepage
        |
        +-- __init__.py
    |
    +-- utils
        |
        +-- __init__.py
    |
    +-- accounts.json
|
+-- .gitattributes
|
+-- .gitignore
|
+-- changelog.md
|
+-- app_dev.md
|
+-- main.py
|
+-- README.md
```

All apps must be built using Python 3 code. Here is an example of an app:

```py
#! python3
# example/__init__.py

from system import utils
from system import homepage


def launch():
    while True:
        utils.make_choice_box('Example',
            ('run code', execute_some_code),
            anything_else=('quit', homepage.launch)
        )

def execute_some_code():
    print("Hello World")
```

Let's dissect it line by line.

1. `from system import utils` and `from system import homepage` import the required modules for this app to function.
2. `launch()` is required for each app. It is like the `main()` function in other languages, the one that will be run.
3. `while True` allows this app to run multiple times.
4. `utils.make_choice_box()` is a function in the `utils` module that provides a fancy choice box at one's convenience. The arguments are:
5. `execute_some_code()` prints "Hello World".

