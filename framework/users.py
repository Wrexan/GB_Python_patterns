class Users:
    def __init__(self, database):
        self.database = database
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

    def get_user(self, username):
        max_id = 1
        for user in self.database.users:
            max_id = max(max_id, user['id'])
            if user['username'] == username:
                return user, max_id
        return None, max_id

    def create_user(self, request, username: str, password: str, tel: str):
        print(f'{request.body=}')
        _user, _max_id = self.get_user(request.body[username])
        if not _user:
            self.database.users.append({'id': _max_id + 1,
                                        'username': request.body[username],
                                        'password': request.body[password],
                                        'tel': request.body[tel],
                                        'courses': []})
            return True, 'Добро пожаловать на наш проект. Приятной учебы.'
        return False, 'Данное имя уже занято.'

    def login_user(self, request, username: str, password: str):
        # print(f'{request.body=}')
        _user, _ = self.get_user(request.body[username])
        if _user:
            if _user['password'] == password:
                _user[''] = 1
            return True, f'Здравствуйте, {_user[username]}.'
        return False, 'Войти не удалось. Возможно такого аккаунта не существует.'
