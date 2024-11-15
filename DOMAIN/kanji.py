#DOMAIN: Se definen entidades principales.

class Kanji:
    def __init__(self, kanji, significado, kunyomi, onyomi, ejemplo):
        self.__kanji = kanji
        self.__onyomi = onyomi
        self.__kunyomi = kunyomi
        self.__significado = significado
        self.__ejemplo = ejemplo

    @property
    def kanji(self):
        return self.__kanji

    @property
    def onyomi(self):
        return self.__onyomi

    @property
    def kunyomi(self):
        return self.__kunyomi

    @property
    def significado(self):
        return self.__significado

    @property
    def ejemplo(self):
        return self.__ejemplo