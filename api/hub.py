from json_users import JSONFile

json_file = JSONFile('./api/users-info.json')


def welcome():
    user = json_file.get()['current_user']
