import tkinter as tk
from frame_interior import FrameInterior


class CanvasNotas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master)

        self.frame_interior = FrameInterior(self)
        self.frame_interior.bind("<Configure>", lambda e: self.configure(scrollregion=self.bbox("all")))

        self.create_window((0, 0), window=self.frame_interior, anchor="nw")
