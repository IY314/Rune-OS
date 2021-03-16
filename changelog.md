# Rune OS ALPHA (3)
## Rune OS ALPHA 3.3
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
