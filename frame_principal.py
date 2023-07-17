from tkinter import ttk

from frame_inferior import FrameInferior
from frame_superior import FrameSuperior
from separador_horizontal import SeparadorHorizontal


class FramePrincipal(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frame_inferior = FrameInferior(self)
        self.frame_superior = FrameSuperior(self, self.frame_inferior)
        self.separador = SeparadorHorizontal(self)

        self.frame_superior.pack(fill='both', expand=True)
        self.separador.pack(side='top', fill='x', padx=5, pady=5)
        self.frame_inferior.pack(fill='both', expand=True)
