from DAL.generic_repository import GenericRepository
from DOMAIN.kanji import Kanji
from pymongo import MongoClient
import os

#DAL: Maneja como y donde se almacenan los datos. Se encarga de leer y escribi datos.

class KanjiDAL(GenericRepository):

    def __init__(self, db_url=None, db_name="KanjiDatabase"):
        db_url = db_url or os.getenv("DB_URL")
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db["kanji"]

    def read(self):
        kanjis = []
        kanji_documents = self.collection.find()

        for doc in kanji_documents:
            # Asegúrate de que el campo ejemplo sea un diccionario
            ejemplo = doc["ejemplo"] if isinstance(doc["ejemplo"], dict) else {"oracion": doc["ejemplo"],
                                                                               "traduccion": ""}

            kanji = Kanji(
                kanji=doc["kanji"],
                onyomi=doc["onyomi"],
                kunyomi=doc["kunyomi"],
                significado=doc["significado"],
                ejemplo=ejemplo
            )
            kanjis.append(kanji)

        return kanjis

    
