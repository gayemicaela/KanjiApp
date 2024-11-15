import tkinter as tk
from tkinter import messagebox
from BLL.user import UserBLL
from form_options import KanjiApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Learn Kanji")
        self.root.geometry("400x500")

        self.user_service = UserBLL()

        # Frame para centrar los widgets
        login_frame = tk.Frame(self.root)
        login_frame.pack(expand=True)
        # LEARN KANJI
        self.lbl_title = tk.Label(login_frame, text="Learn Kanji", font=("Arial", 14))
        self.lbl_title.pack(pady=20)
        # CAMPO USUARIO
        self.lbl_username_login = tk.Label(login_frame, text="Usuario:")
        self.lbl_username_login.pack(pady=5)
        self.ent_username_login = tk.Entry(login_frame)
        self.ent_username_login.pack(pady=5)
        # CAMPO CONTRASEÑA
        self.lbl_password_login = tk.Label(login_frame, text="Contraseña:")
        self.lbl_password_login.pack(pady=5)
        self.ent_password_login = tk.Entry(login_frame, show='*')
        self.ent_password_login.pack(pady=5)
        # BOTON INICIO SESION
        self.btn_login = tk.Button(login_frame, text="Iniciar Sesión", command=self.login)
        self.btn_login.pack(pady=20)
        # BOTON REGISTRO
        self.btn_register = tk.Button(login_frame, text="Registrarse", command=self.open_register_window)
        self.btn_register.pack(pady=5)



    def open_register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Registro")
        register_window.geometry("400x500")

        # Frame para centrar widgets de registro
        register_frame = tk.Frame(register_window)
        register_frame.pack(expand=True)

        lbl_register = tk.Label(register_frame, text="Registro", font=("Arial", 16))
        lbl_register.pack(pady=20)

        # Campos de registro
        lbl_username = tk.Label(register_frame, text="Usuario:")
        lbl_username.pack(pady=5)
        ent_username = tk.Entry(register_frame)
        ent_username.pack(pady=5)

        lbl_password = tk.Label(register_frame, text="Contraseña:")
        lbl_password.pack(pady=5)
        ent_password = tk.Entry(register_frame, show='*')
        ent_password.pack(pady=5)

        lbl_email = tk.Label(register_frame, text="Email:")
        lbl_email.pack(pady=5)
        ent_email = tk.Entry(register_frame)
        ent_email.pack(pady=5)

        # Botón de registro
        btn_register = tk.Button(register_frame, text="Registrarse",
                                 command=lambda: self.register(ent_username.get(), ent_password.get(), ent_email.get(),
                                                               register_window))
        btn_register.pack(pady=20)


    def register(self, username, password, email, register_window):
        if not username or not password or not email:
            messagebox.showwarning("Warning", "Por favor, completa todos los campos.")
            return

        response = self.user_service.register(username, password, email)
        messagebox.showinfo("Registro", response)
        register_window.destroy()  # Cierra la ventana de registro


    def login(self):
        username = self.ent_username_login.get()
        password = self.ent_password_login.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Por favor, completa todos los campos.")
            return

        response = self.user_service.login(username, password)
        messagebox.showinfo("Login", response)

        if response == "Login successful.":
            self.root.destroy()  # Cierra la ventana de login
            new_root = tk.Tk()  # Crea una nueva ventana
            KanjiApp(new_root, username)  # Abre la nueva ventana usando KanjiApp
            new_root.mainloop()




def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()