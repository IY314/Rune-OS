# Rune OS ALPHA (3)
## Rune OS ALPHA 3.6
### Rune OS 3.6.3
- Removed "ALPHA" from Rune OS, version numbers were too confusing when combined
- Fixed a long-running typo in `README.md` and also reformatted it
- Removed obsolete `save()` function from `apps`
- Added password security with the `getpass` module
- Fixed a major bug with file paths in `homepage`
- Reduced the number of global variables in all modules

### Rune OS ALPHA 3.6.2
- Added credits to the bootup text
- Removed "Booting up..." from bootup text
- Added exponentation to the `calc` module
- `tprint()` only supports writing to console, not to files

### Rune OS ALPHA 3.6.1
Publication Update

- Made `main.py` point to the authors of this repository
- Re-added `testing`, `apps`, and added `installation` to `.gitignore`

### Rune OS ALPHA 3.6
- Added `docs.md`
- Removed `example` app and `rosa.txt`
- Adapted `README.md` to redirect to `docs.md`
- Added pre-installed, unremovable app `test` for testing apps
- Added folder `testing` to test apps inside
- Fixed a bug where regular users would not be able to install apps due to a variable being used but not declared
- Temporarily removed `testing` and `apps` from `.gitignore` (they will be re-added later) because GitHub would not recognize the changes otherwise

## Rune OS ALPHA 3.5
### Rune OS ALPHA 3.5.4
- Incremented the bootup text to "3.5.4" (I really need to remember to do this)
- Renamed `extensions` to `installation`
- Added a function `universal_path` to `utils` that takes in a Linux-based path and calls `os.path.join()`
- Wrapped all paths in `universal_path`

### Rune OS ALPHA 3.5.3
Organization Update

- Added new `library` module to `system`
- Moved unused but useful functions (`tprint`, `conceal`, and `repeat`) to `library`
- Added new functions `install`, `uninstall`, and `search` to `extensions`
- `install` installs an app, `uninstall` uninstalls an app, and `search` returns either "local" or "public" depending on whether an app is installed locally or publicly
- Added new action "uninstall app"
- Adapted functions in `homepage` to use the functions in `extensions`

### Rune OS ALPHA 3.5.2
Cleanup Update

- Deleted obsolete `settings` module
- Added a function `tprint` to `utils`, functions like `print` but with realistic typing animation
- Deleted obsolete constant `DEBUG`
- Removed the `ENTER_TEST_MODE` option (it was only used for admin access and 3.5.1 implemented that)
- Fixed an if-else clause to make it require less code
- Fixed several bugs in the `GTN` app (from the time I coded it)

### Rune OS ALPHA 3.5.1
Public apps re-added!

- Re-added public apps (can only be installed by admins)
- Fixed a bug where an app could be installed multiple times
- Added a feature where the first user of the system is an admin
- Added the entire `apps` directory to .gitignore (not deleted though)
- Retitled the bootup text from "RUNE OS ALPHA 3.4" to "RUNE OS ALPHA 3.5.1"
- Added a `clear_console` function to `utils` to clear the console (only when sensible)
- Adapted the `run` function of `apps` to check for both account-specific and public apps
- Fixed a bug where `json_data` was regarded as local so everything broke

### Rune OS ALPHA 3.5
Custom apps!

- Added `extensions` directory for extra apps
- Moved all actions (admin or not) into separate functions in `homepage`
- Moved all apps into `extensions`, can be installed using the "install app" action
- Removed support for public apps (might add later)
- Added new action "install app"
- Added "incorrect password" messages to actions that needed them
- Added `user` to .gitignore (not deleted though)

## Rune OS ALPHA 3.4
### Rune OS ALPHA 3.4.1
Base for custom apps

- Added new app folder `user`
- When a user is created a folder with their username is created in `user`
- Will add support for account-specific apps in the future

### Rune OS ALPHA 3.4
Moved system "apps" to a new directory called `system`.

- Added new directory/package `system`
- Moved `account`, `homepage`, `utils`, and `info.json` into `system`
- Removed obsolete checks for "homepage" and "account" in `homepage`
- Added new `settings` module
- Removed duplicate `account` module in `utils` (no idea why it was there)
- Renamed `changelog.md` into `CHANGELOG.md`
- Retitled the bootup text from "RUNE OS ALPHA 3.3" to "RUNE OS ALPHA 3.4"

## Rune OS ALPHA 3.3
### Rune OS ALPHA 3.3.3
Adds a "delete account" option.

- Added an `update` function to the `account` app to get new information
- Added a "delete account" option to `homepage`

### Rune OS ALPHA 3.3.2
Basically just a cleanup version, removes all unnecessary code.

- Removed the obsolete `__repr__` method from the `Account` class
- Removed the `if __name__ == "__main__"` if-else clauses from every app (the clauses do not actually function)
- Added a description part to the changelog

### Rune OS ALPHA 3.3.1
- Permanently removed the admin action of viewing someone's password
- Updated `README.md` to be less like the RUNE OS TEST `README.md`
- Updated `rosa.txt` to have all necessary files (including `.gitattributes`, `.gitignore`, and `changelog.md`)
- Added all previous changelogs and categorized all changes

### Rune OS ALPHA 3.3
- Removed the soon-deprecated warning
- Removed `dev_main.py` and the `launch` function in `main.py`
- Added password hashing by use of the `hashlib` module
- Temporarily removed the admin action of viewing someone's password

## Rune OS ALPHA 3.2
### Rune OS ALPHA 3.2.3
- Added a soon-deprecated warning for people (like me) who type "3" at the first prompt to create a test account
- Updated the `example` app to support multiple runs
- Fixed the listing of apps in the `run_app` menu to not include the system `account` app
- Added a `dev_main.py` file solely for using the soon-deprecated feature. Running `main.py` normally will not trigger the warning and typing "3" will not work.
- Updated `main.py` to work with `dev_main.py`
- Fixed a bug where duplicate usernames were possible, and only the one created first could be accessed
- Added `changelog.md`
- Added a `dict` attribute to `Account` (for easier account access without having to extract information directly, functions exactly like what is shown in `json_data` )
- Retitled the bootup text from "RUNE OS ALPHA 0.2.2" to "RUNE OS ALPHA 3.2.3"

### Rune OS ALPHA 3.2.2
- Modified `rosa.txt` to redirect to the `example` app for an example
- Created the `example` app, purely for app development although fully functional

### Rune OS ALPHA 3.2.1
- Changed number from 0.2.2.1 to 3.2.1 because it was the third write of Rune OS; second release; first subversion/bugfix version
- Fixed major bug where stored accounts would reset per run (originated 3.1 \[Made `info.json` local\])
- Added newlines at the end of all files that needed them

### Rune OS ALPHA 0.2.2 (3.2)
- Fixed a major bug where logging into an existing account would function opposite to expected
- Added new admin action to view someone's password

## Rune OS ALPHA 0.2.1 (3.1)
### Made `info.json` local (3.1.2)
When the program boots up, it will create a file called `info.json` if there isn't one. If there is one, it will use that. Either way, the accounts are now local to each machine.

### \<untitled\> (3.1.1)
Fixed a major issue where logging in would be available even if there were no accounts

### Update `README.md` (3.1)

### Update `rosa.txt` (3.1)

### Deleted `__pycache__`s (3.1)
#### Deleted ALL the \_\_pycache\_\_

#### Deleted \_\_pycache\_\_

#### Delete \_\_pycache\_\_ directory

### Delete .DS_Store (3.1)

### Update `README.md` (3.1)

### Gitignore (3.1)
