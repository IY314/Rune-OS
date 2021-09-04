from typing import Any, Callable, Dict, List
from api.json_users import JSONFile


def check_special_char(string: str) -> bool:
    for c in string:
        if c in '`~!@#$%^&*()-=_+{}[]\\|;:\'"/?<>,.':
            return True
    return False


class User(object):

    json_file: JSONFile = JSONFile('./api/users-info.json')
    users: List = []
    users_json: List[Dict[str, Any]] = []

    def __init__(self, username: str, password: str, access_level: int = 0) -> None:
        self.username = username
        self.password = hash(password)
        self.access_level = access_level
        self.users.append(self)
        self.users_json.append(self.to_JSON())
        self.json_file.modify('users', self.users_json)

    def to_JSON(self) -> Dict[str, Any]:
        return {
            'username': self.username,
            'password': self.password,
            'access_level': self.access_level
        }

    @classmethod
    def get_info(cls, get_data: Callable, send_data: Callable):
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
    def login(cls, get_data: Callable, send_data: Callable) -> None:
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
            elif hash(data) != found_user.password:
                send_data('failure_p1')
            else:
                cls.json_file.modify('current_user', found_user.to_JSON())
                break
    
    @classmethod
    def change_level(cls, user: Dict[str, Any], level: int = 1) -> None:
        if user not in cls.users_json:
            return
        for u in cls.users:
            if u.username == user['username']:
                u.access_level = level
                break
