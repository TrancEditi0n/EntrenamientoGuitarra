from tkinter import ttk
from canvas_diapason import CanvasDiapason


class FrameCanvas(ttk.Frame):
    def __init__(self, master, numero_cuerdas, numero_trastes, afinacion):
        super().__init__(master)

        self.canvas_diapason = CanvasDiapason(self, numero_cuerdas, numero_trastes, afinacion)
        self.canvas_diapason.pack()
