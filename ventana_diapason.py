import tkinter as tk
from frame_principal_diapason import FramePrincipalDiapason


class VentanaDiapason(tk.Toplevel):
    def __init__(self, master, numero_cuerdas, numero_trastes, afinacion):
        super().__init__(master)

        self.grab_set()
        self.title("Diapasón de la guitarra")
        self.iconbitmap("assets/diapason.ico")
        self.geometry("1500x900")

        self.frame_principal_diapason = FramePrincipalDiapason(self, numero_cuerdas, numero_trastes, afinacion)
        self.frame_principal_diapason.pack(fill='both', expand=True, padx=10, pady=10)
