import getpass
from api import users


def prompt(info):
    print(info)
    return input('>')


def secure_prompt(info):
    print(info)
    return getpass.getpass('>')


def get_field(field_name):
    if field_name == 'username':
        return prompt('Enter a username.')
    elif field_name == 'password':
        return secure_prompt('Enter a secure password.')
    elif field_name == 'try_username':
        return prompt('Username: ')
    elif field_name == 'try_password':
        return secure_prompt('Password: ')


def send_data(data):
    if data == 'failure_u0':
        print('Error: username is too short (must be 4 characters or more)')
    elif data == 'failure_u1':
        print('Error: username is already taken')
    elif data == 'failure_u2':
        print('Error: username not found')
    elif data == 'failure_p0':
        print("Error: password must be 8 characters or more, must contain at "
              "least one special character, and must not contain 'password'")
    elif data == 'failure_p1':
        print('Error: incorrect password')


def main():
    users.User.get_info(get_field, send_data)
    users.User.login(get_field, send_data)
    print(users.User.users)
