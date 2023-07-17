import tkinter as tk
from frame_principal import FramePrincipal


class EntrenamientoDeGuitarraApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw()

        self.title("Entrenamiento de guitarra")
        self.iconbitmap("assets/electric-guitar_icon.ico")

        window_width = 1000
        window_height = 400

        self.minsize(1000, 400)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(True, True)

        self.frame_principal = FramePrincipal(self)
        self.frame_principal.pack(fill='both', expand=True, padx=10, pady=10)
        self.deiconify()
