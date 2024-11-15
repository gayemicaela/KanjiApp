import tkinter as tk
from form_onyomi import OnyomiApp
from form_significados import MeaningsApp
from form_kunyomi import KunyomiApp

class KanjiApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Main Form")
        self.root.geometry("400x500")
        self.username = username

        # Crear un frame principal para centrar todos los widgets
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True)
        # BIENVENIDA
        self.lbl_welcome = tk.Label(main_frame, text="¡Bienvenido!", font=("Arial", 18))
        self.lbl_welcome.pack(pady=20)
        # BOTON KANJI
        self.btn_kanji = tk.Button(main_frame, text="Kanji", font=("Arial", 14), command=self.kanji_action)
        self.btn_kanji.pack(pady=10)
        # BOTON ONYOMI
        self.btn_onyomi = tk.Button(main_frame, text="Onyomi", font=("Arial", 14), command=self.onyomi_action)
        self.btn_onyomi.pack(pady=10)
        # BOTON KUNYOMI
        self.btn_kunyomi = tk.Button(main_frame, text="Kunyomi", font=("Arial", 14), command=self.kunyomi_action)
        self.btn_kunyomi.pack(pady=10)


    def kanji_action(self):
        new_window = tk.Toplevel(self.root)
        MeaningsApp(new_window, self.username)

    def onyomi_action(self):
        new_window = tk.Toplevel(self.root)
        OnyomiApp(new_window, self.username)

    def kunyomi_action(self):
        new_window = tk.Toplevel(self.root)
        KunyomiApp(new_window, self.username)

