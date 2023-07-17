import tkinter as tk
from tkinter import ttk


class Slider(ttk.Scale):
    def __init__(self, master, desde, hasta, largo, defecto):
        super().__init__(master, from_=desde, to=hasta, length=largo, orient=tk.HORIZONTAL)
        self.set(defecto)
