# Rune OS ALPHA Documentation
WIP
(for now just look at `changelog.md`)

## App Development
### Building an App
Your app must be in the `installation` package/folder. If you put it in `apps`, it will very likely be deleted and your app will be gone.

Apps are Python packages (the format is explained below).

Directory:
```
Rune OS
|
+-- apps
    |
    +-- user
        |
        +-- __init__.py
    |
    +-- __init__.py
|
+-- installation
    |
    +-- calc
        |
        +-- __init__.py
    |
    +-- GTN
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
    +-- library
        |
        +-- __init__.py
    |
    +-- utils
        |
        +-- __init__.py
    |
    +-- info.json
|
+-- .gitattributes
|
+-- .gitignore
|
+-- changelog.md
|
+-- docs.md
|
+-- main.py
|
+-- README.md
```

All apps must be built using Python 3 code. Here is an example of an app:

```py
#! python3
# example/__init__.py

def launch():
    while True:
        action = input("Enter 1 to run code.\nEnter anything else to exit.\n>")
        if action == "1":
            execute_some_code()
        else:
            from system import homepage
            homepage.launch()


def execute_some_code():
    print("Hello World")
```

Let's dissect it line by line.

1. `launch()` is required for every app. This is executed whenever the app is launched, hence the name.
2. `while True` ensures that your app will be able to run multiple times in one session (a session is a complete run of the app).
3. `action` takes the user input to decide the next action. This is not required by highly recommended.
4. `if action == "1"` determines if the option inputted in `action` is 1. Be sure to make it into a `str`, or else your app will not function!
5. `execute_some_code()` is not required. It demonstrates that you can have freedom with your app with custom functions, classes, methods, and whatnot.
6. `else` handles the "Enter anything else to exit."
7. `from system import homepage` imports the homepage so your app can return to it.
8. `homepage.launch()` redirects back to the homepage.
9. `execute_some_code()` is a separate function that is called when `action` is 1.
10. `print("Hello World")` demonstrates that the app worked; which is the only real output that it gives.

### Testing an App
The `test` module will help you sniff out bugs in your app. Place your app into the `testing` folder and then run the `test` app.

### Using library functions
The `library` module will provide unused but useful functions for app developers. To use other functions such as `y_n()` and `ask()`, use `utils`. For a more in-depth description, look at the functions' `__doc__`s.

#### Library Functions:
- `tprint()` - a function that prints like a normal human being.
- `conceal()` - a function to conceal a string using a specified letter. Ex: 12345678 -> ****5678.
- `@repeat()` - a decorator to repeat a certain function x times.

#### Utility Functions:
- `ask()` - asks a question.
- `y_n()` - calls `ask()` and returns a boolean value based on the answer.
- `universal_path()` - returns the system-specific path using `os.path.join()`.
- `clear_console()` - clears the console Rune OS is being run on.
