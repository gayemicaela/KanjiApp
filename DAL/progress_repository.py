from pymongo import MongoClient
from DOMAIN.user_progress import UserProgress
import os

class ProgressDAL:
    def __init__(self, db_url=None, db_name="KanjiDatabase"):
        db_url = db_url or os.getenv("DB_URL")
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collections = {
            "meaning": self.db['meaning_progress'],
            "onyomi": self.db["onyomi_progress"],
            "kunyomi": self.db["kunyomi_progress"]
        }

    def save_progress(self, progress_type, username, kanji, errores, correctas):
        collection = self.collections.get(progress_type)

        collection.update_one(
            {"username": username, "kanji": kanji},
            {
                "$set": {
                    "username": username,
                    "kanji": kanji,
                    "errores": errores,
                    "correctas": correctas,
                }
            },
            upsert=True
        )

    def get_user_progress(self, progress_type, username):
        collection = self.collections.get(progress_type)

        records = collection.find({"username": username})
        return [UserProgress(r['username'], r['kanji'], r['errores'], r['correctas']) for r in records]

    def get_kanji_progress(self, progress_type, username, kanji):
        collection = self.collections.get(progress_type)

        record = collection.find_one({"username": username, "kanji": kanji})
        if record:
            return UserProgress(record['username'], record['kanji'], record['errores'], record['correctas'])
        return None