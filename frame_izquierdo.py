import random
import tkinter as tk
from tkinter import ttk

from boton import Boton


class FrameIzquierdo(ttk.Frame):
    notas = ["Ab", "A", "A#", "Bb", "B", "C", "C#", "Db",
             "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#"]

    notasNaturales = ["A", "B", "C", "D", "E", "F", "G"]
    notasAccidentales = ["Ab", "A#", "Bb", "C#", "Db", "D#", "Eb", "F#", "Gb", "G#"]

    def __init__(self, master, frame_inferior):
        super().__init__(master)

        self.frame_inferior = frame_inferior

        self.opciones = (("Generar notas naturales random", 'NNR'),
                         ("Generar notas accidentales random", 'NAR'),
                         ("Generar todas las notas random", 'TNR'),
                         ("Generar 5 notas en cuerdas y trastes", 'NCT'),
                         ("Generar 7 notas aleatorias", 'SNA'))

        self.opcion_elegida = tk.StringVar()

        self.label_seleccion = ttk.Label(self, text="Qué querés generar?")
        self.label_seleccion.pack(fill='x', padx=5, pady=5)

        for opcion in self.opciones:
            radio = ttk.Radiobutton(self, text=opcion[0], value=opcion[1], variable=self.opcion_elegida)
            radio.pack(fill='x', padx=5, pady=5)

        self.opcion_elegida.set("SNA")

        self.boton_generar = Boton(self, "Generar", self.boton_generar_clicked)
        self.boton_generar.pack(fill="x", padx=5, pady=5)

    def boton_generar_clicked(self):

        canvas_notas = self.frame_inferior.canvas_notas
        frame_interior = canvas_notas.frame_interior

        texto = ""

        match self.opcion_elegida.get():
            case "NNR":
                random.shuffle(self.notasNaturales)
                texto = "Notas Naturales Random: " + str(self.notasNaturales)

            case "NAR":
                random.shuffle(self.notasAccidentales)
                texto = "Notas accidentales random: " + str(self.notasAccidentales)

            case "TNR":
                random.shuffle(self.notas)
                texto = "Todas las notas random: " + str(self.notas)

            case "NCT":
                notas_generadas = self.generar_notas(5)
                texto = "\n".join(notas_generadas)

            case "SNA":
                texto = "7 notas random: " + str(random.sample(self.notas, 7))

        label_notas = ttk.Label(frame_interior, text=texto)
        label_notas.pack(fill='x', padx=5, pady=5)
        label_notas.configure(font=("Arial", 16))

        canvas_notas.update_idletasks()
        canvas_notas.yview_moveto(1.0)

    def generar_notas(self, cantidad):

        notas_generadas = []

        for cantidad in range(cantidad):
            nota_random = self.notas[random.randint(0, len(self.notas) - 1)]
            traste_random = random.randint(1, 12)
            cuerda_random = random.randint(2, 7)
            otra_cuerda_random = random.randint(2, 7)

            texto = "Nota: " + nota_random + " Cuerda: " + str(cuerda_random) + "\n" + \
                    "Traste: " + str(traste_random) + " Cuerda: " + str(otra_cuerda_random) + "\n"

            notas_generadas.append(texto)

        return notas_generadas
