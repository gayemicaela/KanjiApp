from DAL.user_repository import UserDAL
import bcrypt

class UserBLL:
    def __init__(self):
        self.user_repository = UserDAL()

    def obtener_users(self):
        user_data = self.user_repository.read()

        user_list = []
        for user in user_data:
            try:
                user_list.append(user)
            except KeyError as e:
                print(f"Error procesando el user: {e}")
        return user_list

    def register(self, username, password, email):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return self.user_repository.add_user(username, hashed_password, email)

    def login(self, username, password):
        users = self.user_repository.read()
        for user in users:
            if user.username == username:
                if bcrypt.checkpw(password.encode('utf-8'), user.password): 
                    return "Login successful."
                else:
                    return "Invalid password."
        return "Invalid username."