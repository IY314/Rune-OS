import sys
import os
import hashlib
import getpass
import json
from system import utils


class JSONFile(utils.File):

    def update(self):
        DEFAULT_JSON_DATA = {'CURRENT': None, 'ACCOUNTS': []}
        try:
            with open(self.filename.path) as f:
                self.data = json.loads(f.read())
        except FileNotFoundError:
            with open(self.filename.path, 'w+') as f:
                f.write(json.dumps(DEFAULT_JSON_DATA))
                self.data = DEFAULT_JSON_DATA

        del f


data = JSONFile('system/accounts.json')


class Account:
    params = { 'username', 'password', 'has_admin' }

    def __init__(self, *, username=None, password=None):
        unidentified = []

        if username is not None:
            self.username = username
        else:
            unidentified.append('username')
        if password is not None:
            self.password = password
        else:
            unidentified.append('password')

        self.get_info(*unidentified, 'has_admin')
        self.dict = {
            'username': self.username,
            'password': self.password,
            'has_admin': self.has_admin
        }
        data.data['ACCOUNTS'].append(self.dict)
        os.makedirs(utils.Path.universal_path(f'apps/private/{self.username}'))
        with open(utils.Path.universal_path(f'apps/private/{self.username}/__init__.py'), 'w+'):
            pass
        data.save()

    def get_info(self, *fields):
        def username():
            while True:
                possible_username = utils.ask('Enter a username.')
                for user in data.data['ACCOUNTS']:
                    if possible_username == user['username']:
                        print('That username is taken.')
                        break
                else:
                    self.username = possible_username
                    break

        def password():
            self.password = hashlib.sha256(utils.ask('Enter a secure password.', confirm=2,
                confirm_response='Type it again.', min_letters=8).encode('utf-8')).hexdigest()

        def has_admin():
            self.has_admin = True if data.data['ACCOUNTS'] == [] else False

        for field in fields:
            if field == 'username':
                username()
            elif field == 'password':
                password()
            elif field == 'has_admin':
                has_admin()
            else:
                raise utils.ProgrammerError('Invalid field')


def login(clear=True):
    def create_account():
        utils.clear_console()
        new_account = Account()
        utils.dummy(new_account)
        data.data['CURRENT'] = new_account.dict
        data.save()
        from system import homepage
        return homepage.launch()

    def login_account():
        data.update()
        return match_account()

    def match_account(clear=True):
        if clear: utils.clear_console()
        username = input('Username: ')
        for a in data.data['ACCOUNTS']:
            if username == '':
                return login()
            if username == a['username']:
                selected_account = a
                return match_password(selected_account, False)
        else:
            print('Invalid account.')
            return match_account(False)

    def match_password(selected_account, clear=True):
        if clear: utils.clear_console()
        password = getpass.getpass('Password: ')
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if password == '':
            return match_account()
        elif hashed != selected_account['password']:
            print('Incorrect password.')
            return match_password(selected_account, False)
        else:
            data.data['CURRENT'] = selected_account
            data.save()
            from system import homepage
            return homepage.launch()

    if clear: utils.clear_console()

    utils.make_choice_box('Login',
        ('create a new account', create_account),
        ('login to an existing account', login_account, True),
        anything_else=('shut down', exit), condition=data.data['ACCOUNTS'] != []
    )
