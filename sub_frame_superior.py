import tkinter as tk
from tkinter import ttk
from boton import Boton
from combo_box import ComboBox
from ventana_diapason import VentanaDiapason
from ventana_seleccion_afinacion import VentanaSeleccionAfinacion


class SubFrameSuperior(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        self.opciones_cuerdas = [4, 5, 6, 7, 8, 9, 10]
        self.opciones_trastes = [7, 9, 12, 15, 17, 19, 21, 24]
        self.opciones_afinacion = (("Afinación Estandar", 'AE'),
                                   ("Seleccionar Afinación personalizada...", 'AP'))
        self.opcion_afinacion_elegida = tk.StringVar()

        self.afinacion_estandar = [('E', 4), ('B', 3), ('G', 3), ('D', 3), ('A', 2), ('E', 2), ('B', 1), ('F#', 1), ('C#', 1), ('G#', 0)]
        self.afinacion_personalizada = []

        self.combo_cuerdas = ComboBox(self, self.opciones_cuerdas, 7)
        self.combo_trastes = ComboBox(self, self.opciones_trastes, 24)
        self.label_cuerdas = ttk.Label(self, text="Cantidad de cuerdas:")
        self.label_trastes = ttk.Label(self, text="Cantidad de trastes:")
        self.label_afinacion = ttk.Label(self, text="Seleccionar afinación:")

        self.label_cuerdas.grid(row=0, column=0)
        self.combo_cuerdas.grid(row=1, column=0)
        self.label_trastes.grid(row=2, column=0)
        self.combo_trastes.grid(row=3, column=0)
        self.label_afinacion.grid(row=0, column=1)

        fila_opciones_afinacion = 1

        for opcion in self.opciones_afinacion:
            radio = ttk.Radiobutton(self, text=opcion[0], value=opcion[1], variable=self.opcion_afinacion_elegida)
            radio.grid(row=fila_opciones_afinacion, column=1, sticky="w")
            fila_opciones_afinacion += 1

        self.opcion_afinacion_elegida.set("AE")

        self.boton_mostrar_diapason = Boton(self, "Mostrar Diapasón", self.boton_mostrar_diapason_clicked)
        self.boton_mostrar_diapason.grid(row=4, column=0, columnspan=2)

    def boton_mostrar_diapason_clicked(self):

        numero_cuerdas = int(self.combo_cuerdas.get())
        numero_trastes = int(self.combo_trastes.get())

        if self.opcion_afinacion_elegida.get() == "AE":
            VentanaDiapason(self, numero_cuerdas, numero_trastes, self.afinacion_estandar)
        elif self.opcion_afinacion_elegida.get() == "AP":
            ventana_seleccion_afinacion = VentanaSeleccionAfinacion(self, numero_cuerdas)
            print(self.afinacion_personalizada)
            self.wait_window(ventana_seleccion_afinacion)
            VentanaDiapason(self, numero_cuerdas, numero_trastes, self.afinacion_personalizada)
