## Rune OS ALPHA 3.2.3
- Added a soon-deprecated warning for people (like me) who type "3" at the first prompt to create a test account
- Updated the `example` app to support multiple runs
- Fixed the listing of apps in the `run_app` menu to not include the system `account` app
- Added a `dev_main.py` file solely for using the soon-deprecated feature. Running `main.py` normally will not trigger the warning and typing "3" will not work.
- Updated `main.py` to work with `dev_main.py`
- Fixed a bug where duplicate usernames were possible, and only the one created first could be accessed
- Added `changelog.md`
- Added a `dict` attribute to `Account` (for easier account access without having to extract information directly, functions exactly like what is shown in `json_data` )
- Retitled the bootup text from "RUNE OS ALPHA 0.2.2" to "RUNE OS ALPHA 3.2.3"
