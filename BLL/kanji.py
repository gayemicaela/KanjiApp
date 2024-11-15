from DAL.kanji_repository import KanjiDAL
import random

#BLL: Toma los datos proporcionados por la DAL, aplica la lógica necesaria y luego pasa esos datos a la capa de presentacion (Form Principal)


class KanjiBLL:
    def __init__(self):
        # Inicializa el repositorio DAL internamente
        self.kanji_repository = KanjiDAL()

    def obtener_kanjis(self):
        kanji_data = self.kanji_repository.read()

        kanji_list = []
        for kanji in kanji_data:
            try:
                kanji_list.append(kanji)
            except KeyError as e:
                print(f"Error procesando el kanji: {e}")
        return kanji_list

    def get_random_kanji(self):
        kanjis = self.kanji_repository.read()
        if kanjis:
            return random.choice(kanjis)
