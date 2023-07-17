from tkinter import ttk
from frame_canvas import FrameCanvas
from frame_seleccion_ejercicio import FrameSeleccionEjercicio


class FrameDiapason(ttk.Frame):
    def __init__(self, master, numero_cuerdas, numero_trastes):
        super().__init__(master)

        self.frame_canvas = FrameCanvas(self, numero_cuerdas, numero_trastes)
        self.frame_seleccion_ejercicio = FrameSeleccionEjercicio(self)

        self.frame_canvas.pack()
        self.frame_seleccion_ejercicio.pack(fill='both', expand=True)
