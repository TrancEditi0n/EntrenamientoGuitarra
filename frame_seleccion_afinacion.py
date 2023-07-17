from tkinter import ttk
from boton import Boton
from combo_box import ComboBox


class FrameSeleccionAfinacion(ttk.Frame):
    def __init__(self, master, numero_cuerdas):
        super().__init__(master)

        self.label_afinacion = ttk.Label(self, text="Selecciona la afinación para cada cuerda:")
        self.label_afinacion.grid(row=0, columnspan=3)

        self.afinacion_estandar = [('E', 4), ('B', 3), ('G', 3), ('D', 3), ('A', 2), ('E', 2), ('B', 1), ('F#', 1),
                              ('C#', 1), ('G#', 0)]

        self.comboboxes_notas = []
        self.comboboxes_octavas = []

        for cuerda in range(numero_cuerdas):

            self.label_cuerda = ttk.Label(self, text="Cuerda " + str(cuerda + 1))
            self.label_cuerda.grid(row=cuerda + 1, column=0)

            self.combobox_nota = ComboBox(self, ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], self.afinacion_estandar[cuerda][0])
            self.combobox_nota.grid(row=cuerda + 1, column=1)
            self.comboboxes_notas.append(self.combobox_nota)

            self.combobox_octava = ComboBox(self, [0, 1, 2, 3, 4, 5, 6, 7, 8], self.afinacion_estandar[cuerda][1])
            self.combobox_octava.grid(row=cuerda + 1, column=2)
            self.comboboxes_octavas.append(self.combobox_octava)

        self.boton_confirmar = Boton(self, "Confirmar Afinación", self.boton_confirmar_clicked)
        self.boton_confirmar.grid(row=numero_cuerdas + 1, columnspan=3)

    def boton_confirmar_clicked(self):

        afinacion_personalizada = []

        for cuerda in range(len(self.comboboxes_notas)):
            tupla_nota_octava = self.comboboxes_notas[cuerda].get(), int(self.comboboxes_octavas[cuerda].get())
            afinacion_personalizada.append(tupla_nota_octava)

        self.master.master.afinacion_personalizada = afinacion_personalizada
        self.master.destroy()
