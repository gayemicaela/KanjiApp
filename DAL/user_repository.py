from DAL.generic_repository import GenericRepository
from DOMAIN.user import User
from pymongo import MongoClient
import os

class UserDAL(GenericRepository):

    def __init__(self, db_url=None, db_name="KanjiDatabase"):
        db_url = db_url or os.getenv("DB_URL")
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db["user"]

    def read(self):
        users = []
        for user_data in self.collection.find({}, {"_id": 0}):
            user = User(username=user_data['username'], password=user_data['password'], email=user_data['email'])
            users.append(user)
        return users

    def add_user(self, username, password, email):
        if self.collection.find_one({"username": username}):
            raise Exception(f"User {username} already exists.")

        self.collection.insert_one({
            "username": username,
            "password": password,
            "email": email
        })

        return "Usuario agregado correctamente."