class UserProgress:

    def __init__(self, username, kanji, errores = 0, correctas = 0, revisado=False):
        self.__username = username
        self.__kanji = kanji
        self.__errores = errores
        self.__correctas = correctas
        self.__revisado = revisado

    @property
    def username(self):
        return self.__username

    @property
    def kanji(self):
        return self.__kanji

    @property
    def errores(self):
        return self.__errores

    @property
    def correctas(self):
        return self.__correctas

    @property
    def revisado(self):
        return self.__revisado

    def registrar_error(self):
        self.__errores += 1

    def registrar_acierto(self):
        self.__correctas += 1
        if self.__correctas > 3:
            self.__revisado = True


