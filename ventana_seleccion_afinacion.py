import tkinter as tk
from frame_seleccion_afinacion import FrameSeleccionAfinacion


class VentanaSeleccionAfinacion(tk.Toplevel):
    def __init__(self, master, numero_cuerdas):
        super().__init__(master)

        self.grab_set()
        self.withdraw()
        self.title("Seleccionar Afinacion")
        self.iconbitmap("assets/diapason.ico")
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width - self.winfo_reqwidth()) / 2)
        y = int((screen_height - self.winfo_reqheight()) / 2)

        self.geometry(f"+{x}+{y}")

        self.frame_seleccion_afinacion = FrameSeleccionAfinacion(self, numero_cuerdas)
        self.frame_seleccion_afinacion.pack(fill='both', expand=True, padx=10, pady=10)

        self.deiconify()