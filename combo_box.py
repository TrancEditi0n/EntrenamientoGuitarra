from tkinter import ttk


class ComboBox(ttk.Combobox):
    def __init__(self, master, opciones, opcion_por_defecto):
        super().__init__(master, state="readonly")
        self['values'] = opciones
        self.set(opcion_por_defecto)
