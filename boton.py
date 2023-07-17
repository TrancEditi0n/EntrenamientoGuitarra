from tkinter import ttk


class Boton(ttk.Button):
    def __init__(self, master, text, command):
        super().__init__(master, text=text, command=command)
