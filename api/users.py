import hashlib
from dataclasses import dataclass
from typing import ClassVar
from api.json_users import JSONFile


def check_special_char(string: str) -> bool:
    for c in string:
        if c in '`~!@#$%^&*()-=_+{}[]\\|;:\'"/?<>,.':
            return True
    return False


@dataclass
class User:
    json_file: ClassVar = JSONFile('./api/users-info.json')
    users: ClassVar = []
    users_json: ClassVar = []

    username: str
    password: str
    access_level: int = 0

    def __post_init__(self):
        self.password = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
        self.users.append(self)
        self.users_json.append(self.to_JSON())
        self.json_file.modify('users', self.users_json)

    def to_JSON(self):
        return {
            'username': self.username,
            'password': self.password,
            'access_level': self.access_level
        }

    @classmethod
    def get_info(cls, get_data, send_data):
        while True:
            data = get_data('username')
            if len(data) < 4:
                send_data('failure_u0')
                continue
            elif data in (u.username for u in cls.users):
                send_data('failure_u1')
                continue
            username = str(data)
            break
        while True:
            data = get_data('password')
            if len(data) < 8 or not check_special_char(data) \
            or 'password' in data:
                send_data('failure_p0')
                continue
            password = str(data)
            break
        access_level = 2 if not cls.users else 0

        return User(username, password, access_level)

    @classmethod
    def login(cls, get_data, send_data):
        found_user = None
        while True:
            data = get_data('try_username')
            for user in cls.users:
                if user.username == data:
                    found_user = user
                    break
            else:
                send_data('failure_u2')
                continue
            break
        while True:
            data = get_data('try_password')
            if data is None:
                return cls.login(get_data, send_data)
            elif hashlib.sha256(data.encode('utf-8')).hexdigest() != found_user.password:
                send_data('failure_p1')
            else:
                cls.json_file.modify('current_user', found_user.to_JSON())
                break

    @classmethod
    def change_level(cls, user, level=1):
        if user not in cls.users_json:
            return
        for u in cls.users:
            if u.username == user['username']:
                u.access_level = level
                break
