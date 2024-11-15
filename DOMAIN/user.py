class User:

    def __init__(self, username, password, email, user_id=None):
        self.__id = user_id
        self.__username = username
        self.__password = password
        self.__email = email

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def email(self):
        return self.__email