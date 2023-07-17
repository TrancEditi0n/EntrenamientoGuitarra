from tkinter import ttk


class SeparadorVertical(ttk.Separator):
    def __init__(self, master):
        super().__init__(master, orient='vertical')
