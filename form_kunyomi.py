import tkinter as tk
from tkinter import messagebox
from BLL.kanji import KanjiBLL
import random
from BLL.progress import ProgressLogic

class KunyomiApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Kunyomi Quiz")
        self.root.geometry("400x500")

        self.username = username
        self.kanji_service = KanjiBLL()
        self.progress_service = ProgressLogic()

        self.kanji_actual = None
        self.opciones = None

        # Cargar Kanjis
        try:
            self.lista_kanjis = self.kanji_service.obtener_kanjis()
            if not self.lista_kanjis:
                messagebox.showerror("Error", "El archivo está vacío o no se pudieron obtener kanjis.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener los kanjis: {e}")
            return

        # Crear un frame principal para centrar todos los widgets
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True)
        # KANJI
        self.kanji_label = tk.Label(main_frame, text="", font=("Arial", 100))
        self.kanji_label.pack(pady=20)
        # FRAME PARA BOTONES
        self.boton_frame = tk.Frame(main_frame)
        self.boton_frame.pack(pady=10)

        kanji_frame = tk.Frame(self.root)
        kanji_frame.pack(expand=True)
        # CREAR BOTONES
        self.boton1 = tk.Button(self.boton_frame, text="", font=("Arial", 14),
                                command=lambda: self.verificar_respuesta(0), width=10)
        self.boton1.grid(row=0, column=0, padx=5, sticky='ew')

        self.boton2 = tk.Button(self.boton_frame, text="", font=("Arial", 14),
                                command=lambda: self.verificar_respuesta(1), width=10)
        self.boton2.grid(row=0, column=1, padx=5, sticky='ew')

        self.boton3 = tk.Button(self.boton_frame, text="", font=("Arial", 14),
                                command=lambda: self.verificar_respuesta(2), width=10)
        self.boton3.grid(row=1, column=0, padx=5, sticky='ew')

        self.boton4 = tk.Button(self.boton_frame, text="", font=("Arial", 14),
                                command=lambda: self.verificar_respuesta(3), width=10)
        self.boton4.grid(row=1, column=1, padx=5, sticky='ew')
        # BOTON HISTORIAL
        self.check_button = tk.Button(kanji_frame, text="Ver historial", font=("Arial", 14), padx=10, pady=10)
        self.check_button.pack(pady=10)
        self.check_button.config(command=self.mostrar_historial)
        # MOSTRAR KANJI
        self.mostrar_nuevo_kanji()


    def mostrar_historial(self):
        history = self.progress_service.get_user_progress_history("kunyomi", self.username)

        unique_kanjis = {}
        for entry in history:
            kanji = entry['kanji']
            if kanji not in unique_kanjis:
                unique_kanjis[kanji] = entry

        # FORM
        history_window = tk.Toplevel(self.root)
        history_window.title("Historial de Progreso")
        history_window.geometry("400x500")

        # HISTORIAL DE PROGRESO
        title_label = tk.Label(history_window, text="Historial de Progreso", font=("Arial", 16))
        title_label.pack(pady=10)

        # SCROLLBAR
        canvas = tk.Canvas(history_window, width=360, height=400)
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollable_frame = tk.Frame(canvas)

        scrollbar = tk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # AJUSTE DE CONTENIDO
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # EVENTO
        def _on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
        history_window.protocol("WM_DELETE_WINDOW",
                                lambda: canvas.unbind_all("<MouseWheel>") or history_window.destroy())

        # HISTORIAL Y BARRA DE PROGRESO
        for kanji, entry in unique_kanjis.items():
            frame = tk.Frame(scrollable_frame)
            frame.pack(anchor='w', pady=5)

            # DETALLE
            entry_text = f"Kanji: {kanji} - Errores: {entry['errores']}, Correctas: {entry['correctas']}"
            label = tk.Label(frame, text=entry_text)
            label.pack(anchor='w')

            # CALCULO PROPORCIONES
            total_respuestas = entry['errores'] + entry['correctas']
            correctas_proporcion = (entry['correctas'] / total_respuestas) if total_respuestas > 0 else 0

            # BARRA DE PROGRESO
            progress_bar = tk.Canvas(frame, width=340, height=20)
            progress_bar.pack()
            # PARTE ROJA
            progress_bar.create_rectangle(0, 0, 340 * correctas_proporcion, 20, fill="green")
            # PARTE VERDE
            progress_bar.create_rectangle(340 * correctas_proporcion, 0, 340, 20, fill="red")

        # BOTON CERRAR
        close_button = tk.Button(history_window, text="Cerrar", command=history_window.destroy)
        close_button.pack(pady=10)



    def mostrar_nuevo_kanji(self):
        # Obtener un kanji aleatorio
        self.kanji_actual = self.kanji_service.get_random_kanji()
        self.kanji_label.config(text=self.kanji_actual.kanji)
        self.mostrar_opciones_kunyomi()


    def mostrar_opciones_kunyomi(self):
        self.opciones = set()  # Usar un conjunto para evitar duplicados

        self.opciones.add(self.kanji_actual.kunyomi)

        while len(self.opciones) < 4:
            try:
                nuevo_kanji = self.kanji_service.get_random_kanji()
                if nuevo_kanji.kunyomi != self.kanji_actual.kunyomi:
                    self.opciones.add(nuevo_kanji.kunyomi)
            except ValueError:
                break

        self.opciones = list(self.opciones)
        random.shuffle(self.opciones)

        # Asignar texto a los botones
        self.boton1.config(text=self.opciones[0])
        self.boton2.config(text=self.opciones[1])
        self.boton3.config(text=self.opciones[2])
        self.boton4.config(text=self.opciones[3])


    def verificar_respuesta(self, opcion):
        if self.opciones[opcion] == self.kanji_actual.kunyomi:
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            self.progress_service.update_progress("kunyomi", self.username, self.kanji_actual.kanji, is_correct=True)
        else:
            messagebox.showerror("Incorrecto", f"Incorrecto. La respuesta correcta es: {self.kanji_actual.kunyomi}")
            self.progress_service.update_progress("kunyomi", self.username, self.kanji_actual.kanji, is_correct=False)

        # Mostrar un nuevo kanji
        self.mostrar_nuevo_kanji()
