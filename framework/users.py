from secrets import token_hex

from database import DB


class Users:
    def __init__(self):
        self.database = DB

    #     self.__username: str = ''
    #     self.__password: str = ''
    #     # self.__firstname: str = ''
    #     # self.__lastname: str = ''
    #     self.__tel: str = ''
    #     self.__courses: dict = {}
    #
    # @property
    # def username(self):
    #     return self.__username
    #
    # @username.setter
    # def username(self, username):
    #     if not isinstance(username, str):
    #         print(f'Name must be a string: {username}')
    #     if len(username) < 3 or len(username) > 16:
    #         print(f'Length of username {username} must be 3-16')
    #     self.__username = username
    #
    # @property
    # def password(self):
    #     return self.__password
    #
    # @password.setter
    # def password(self, password):
    #     if not isinstance(password, str):
    #         print(f'Password must be a string: {password}')
    #     if len(password) < 3 or len(password) > 16:
    #         print(f'Length of password {password} must be 3-16')
    #     self.__password = password
    #
    # @property
    # def tel(self):
    #     return self.__tel
    #
    # @tel.setter
    # def tel(self, tel):
    #     if not isinstance(tel, str):
    #         print(f'Tel must be a string: {tel}')
    #     if len(tel) < 7 or len(tel) > 10:
    #         print(f'Length of tel {tel} must be 7-10')
    #     self.__tel = tel
    #
    # @property
    # def courses(self):
    #     return self.__courses
    #
    # # @add_course.setter
    # def add_course(self, __id):
    #     if self.check_course(__id):
    #         self.__courses[__id] = __id
    #
    # def del_course(self, __id):
    #     if self.check_course(__id):
    #         del self.__courses[__id]
    #
    # @staticmethod
    # def check_course(__id):
    #     if not isinstance(__id, int):
    #         print(f'Course id must be an integer: {__id}')
    #     if __id <= 0:
    #         print(f'Course id must be higher than 0: {__id}')
    #     return True

    def check_user_token(self, username, token):
        for user in self.database.users:
            if user['username'] == username:
                if user['token'] == token:
                    return True
                return False
        return None

    def get_user_max_id(self, username):
        max_id = 1
        for user in self.database.users:
            max_id = max(max_id, user['id'])
            if user['username'] == username:
                return user, max_id
        return None, max_id

    def create_user(self, request):
        # print(f'{request.body=} {username=}')
        if request.reg is None or \
                'username' not in request.reg or request.reg['username'] == '' \
                                                                            'password' not in request.reg or \
                request.reg['password'] == '' \
                                           'tel' not in request.reg or request.reg['tel'] == '':
            print(f'ERROR on register: В запросе отсутствует(ют) поля : {request.reg=}')
            return False, f'Заполните обязательные поля'
        _user, _max_id = self.get_user_max_id(request.reg['username'])
        if not _user:
            _email = request.reg['email'] if 'email' in request.reg else ''
            self.database.users.append({'id': _max_id + 1,
                                        'username': request.reg['username'],
                                        'password': request.reg['password'],
                                        'tel': request.reg['tel'],
                                        'email': _email,
                                        'courses': []})
            return True, f'Добро пожаловать на наш проект, {request.reg["username"]}. Приятной учебы.'
        return False, 'Данное имя уже занято.'

    def login_user(self, request, reg_login: bool = False):
        # print(f'{request.auth=} {type(request.auth)=}')
        auth = request.reg if reg_login else request.auth
        if 'username' in auth and 'password' in auth:
            _user, _ = self.get_user_max_id(auth['username'])
            if _user:
                if _user['password'] == auth['password']:
                    if _user['token'] == '':
                        _user['token'] = str(token_hex(16))
                    request.send_headers['HTTP_AUTHORIZATION'] = f'{_user["username"]}:{_user["token"]}'
                    # request.send_headers['HTTP_AUTHORIZATION'] = f'Bearer {_user["username"]}:{_user["token"]}'
                    return True, f'Здравствуйте, {_user["username"]}<br>Добро пожаловать на наши курсы'
                return False, 'Неправильный пароль.'
        return False, 'Аккаунта с таким именем не существует'

    def logout_user(self, request, reg_login: bool = False):
        if request.verified:
            try:
                for _user in DB.users:
                    if _user['username'] == [request.verified[1]]:
                        _user['token'] = ''
                request.verified = None, None
            except Exception as e:
                print(f'Не удалось разлогинить аккаунт {request.verified[1]} по причине: {e}')

U = Users()
