from tkinter import ttk
from frame_cronometro import FrameCronometro
from slider import Slider


class FrameVolumenYCronometro(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_volumen = ttk.Label(self, text="Volumen:")
        self.slider_volumen = Slider(self, 0, 100, 100, 100)

        self.label_volumen.pack(fill='y', padx=5, pady=5)
        self.slider_volumen.pack()

        self.frame_cronometro = FrameCronometro(self)
        self.frame_cronometro.pack()
