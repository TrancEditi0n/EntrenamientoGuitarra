from tkinter import ttk
from separador_horizontal import SeparadorHorizontal
from sub_frame_inferior import SubFrameInferior
from sub_frame_superior import SubFrameSuperior


class FrameDerecho(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.subframe_superior = SubFrameSuperior(self)
        self.subframe_inferior = SubFrameInferior(self)
        self.separador_sub_frames = SeparadorHorizontal(self)

        self.subframe_superior.pack(fill='both', expand=True)
        self.separador_sub_frames.pack(side='top', fill='x', padx=5, pady=5)
        self.subframe_inferior.pack(fill='both', expand=True)
