from system import account, utils

VERSION = 'Rune OS 3.8.2'
CREDITS = 'Made by @IY314 and @mrfoogles'
LINK = 'https://github.com/IY314/Rune-OS'

print(utils.make_box(VERSION, CREDITS, LINK, form='centered'))
account.login(False)
