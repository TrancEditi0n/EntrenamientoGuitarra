from tkinter import ttk
from frame_derecho import FrameDerecho
from frame_izquierdo import FrameIzquierdo
from separador_vertical import SeparadorVertical


class FrameSuperior(ttk.Frame):
    def __init__(self, master, frame_inferior):
        super().__init__(master)

        self.frame_izquierdo = FrameIzquierdo(self, frame_inferior)
        self.frame_izquierdo.pack(fill='both', expand=True, side='left')

        self.separador_vertical = SeparadorVertical(self)
        self.separador_vertical.pack(side='left', fill='y', padx=5, pady=5)

        self.frame_derecho = FrameDerecho(self)
        self.frame_derecho.pack(fill='both', expand=True, side='right')
