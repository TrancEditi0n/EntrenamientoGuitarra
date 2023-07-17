from tkinter import ttk


class SeparadorHorizontal(ttk.Separator):
    def __init__(self, master):
        super().__init__(master, orient='horizontal')
