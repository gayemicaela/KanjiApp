import tkinter as tk
from tkinter import messagebox
from BLL.kanji import KanjiBLL
from BLL.progress import ProgressLogic


class MeaningsApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Learn Kanji")
        self.root.geometry("400x500")

        self.username = username
        self.kanji_service = KanjiBLL()
        self.progress_service = ProgressLogic()

        self.kanji_actual = None


        # Cargar Kanjis
        try:
            self.lista_kanjis = self.kanji_service.obtener_kanjis
            if not self.lista_kanjis:
                messagebox.showerror("Error", "El archivo está vacío o no se pudieron obtener kanjis.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener los kanjis: {e}")
            return


        # Crear un frame para centrar los widgets
        kanji_frame = tk.Frame(self.root)
        kanji_frame.pack(expand=True)
        #KANJI
        self.kanji_label = tk.Label(kanji_frame, text="", font=("Arial", 100))
        self.kanji_label.pack(pady=20)
        #SIGNIFICADO
        self.input_significado = tk.Entry(kanji_frame, font=("Arial", 16), width=20)
        self.input_significado.pack(pady=10)
        # BOTON VERIFICAR
        self.check_button = tk.Button(kanji_frame, text="Verificar", font=("Arial", 14), padx=10, pady=10)
        self.check_button.pack(pady=10)
        self.check_button.config(command=self.verificar_significado)
        # BOTON HISTORIAL
        self.check_button = tk.Button(kanji_frame, text="Ver historial", font=("Arial", 14), padx=10, pady=10)
        self.check_button.pack(pady=10)
        self.check_button.config(command=self.mostrar_historial)
        # MOSTRAR KANJI
        self.mostrar_nuevo_kanji()

    def mostrar_historial(self):
        history = self.progress_service.get_user_progress_history("meaning", self.username)

        # Filtrar para obtener solo kanjis únicos
        unique_kanjis = {}
        for entry in history:
            kanji = entry['kanji']
            if kanji not in unique_kanjis:
                unique_kanjis[kanji] = entry  # Guarda la entrada completa

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

    def verificar_significado(self):
        significado_usuario = self.input_significado.get().strip().lower()  # Convertir a minúsculas
        if significado_usuario == self.kanji_actual.significado.lower():  # Comparar en minúsculas
            messagebox.showinfo(
                "Correcto",
                f"¡Correcto! \nEjemplo: {self.kanji_actual.ejemplo['oracion']}\nTraducción: {self.kanji_actual.ejemplo['traduccion']}"
            )
            self.progress_service.update_progress("meaning", self.username, self.kanji_actual.kanji, is_correct=True)
        else:
            messagebox.showerror(
                "Incorrecto",
                f"Incorrecto. La respuesta es: {self.kanji_actual.significado}"
            )
            self.progress_service.update_progress("meaning", self.username, self.kanji_actual.kanji, is_correct=False)


        # Limpiar el campo de entrada y mostrar un nuevo kanji
        self.input_significado.delete(0, tk.END)
        self.mostrar_nuevo_kanji()

