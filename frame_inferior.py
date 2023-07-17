from tkinter import ttk
from canvas_notas import CanvasNotas


class FrameInferior(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.canvas_notas = CanvasNotas(self)
        self.canvas_notas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas_notas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas_notas.configure(yscrollcommand=self.scrollbar.set)
