from tkinter import ttk
from frame_metronomo import FrameMetronomo
from frame_volumen_y_cronometro import FrameVolumenYCronometro


class SubFrameInferior(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frame_volumen = FrameVolumenYCronometro(self)
        self.frame_metronomo = FrameMetronomo(self, self.frame_volumen)
        self.frame_volumen.pack(fill='both', expand=True, side='left')
        self.frame_metronomo.pack(fill='both', expand=True, side='right')
