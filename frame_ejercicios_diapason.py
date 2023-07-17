import threading
import time
import tkinter as tk
import fluidsynth
from tkinter import ttk


class FrameEjerciciosDiapason(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        intervalos = ["Unísono", "Segunda Menor", "Segunda Mayor", "Tercera Menor", "Tercera Mayor",
                      "Cuarta Justa", "Tritono", "Quinta Justa", "Sexta Menor", "Sexta Mayor",
                      "Séptima Menor", "Séptima Mayor", "Octava"]

        self.botones_intervalos = []
        self.respuestas_correctas = 0
        self.respuestas_incorrectas = 0
        self.porcentaje_respuestas_correctas = 0
        self.total_ejercicios = 0

        for intervalo in intervalos:
            boton_intervalo = tk.Button(self, text=intervalo, font=("Arial", 12), state="disabled")
            boton_intervalo.config(command=lambda boton=boton_intervalo: self.verificar_intervalo(boton))
            self.botones_intervalos.append(boton_intervalo)
            boton_intervalo.pack(side="left", expand=True, fill="both")

    def verificar_intervalo(self, boton_intervalo):

        texto_boton = boton_intervalo.cget("text")

        frame_principal = self.master
        intervalo_actual = frame_principal.intervalo

        nota_1 = frame_principal.nota_1
        nota_2 = frame_principal.nota_2

        frame_seleccion_ejercicio = self.master.frame_superior_diapason.frame_seleccion_ejercicio

        label_respuestas_correctas = frame_seleccion_ejercicio.label_respuestas_correctas
        label_respuestas_incorrectas = frame_seleccion_ejercicio.label_respuestas_incorrectas
        label_porcentaje_respuestas_correctas = frame_seleccion_ejercicio.label_porcentaje_respuestas_correctas

        if intervalo_actual == texto_boton:
            boton_intervalo.configure(bg="green", activebackground="green", fg="white")
            threading.Thread(target=self.reproducir_notas, args=(nota_1, nota_2), daemon=True).start()
            threading.Thread(target=self.restablecer_color_original, daemon=True).start()
            threading.Thread(target=self.mostrar_siguiente_intervalo, daemon=True).start()
            self.respuestas_correctas += 1
            label_respuestas_correctas.configure(text="Respuestas correctas: " + str(self.respuestas_correctas))

        else:
            boton_intervalo.configure(bg="red", activebackground="red")
            boton_intervalo.configure(state="disabled")
            self.respuestas_incorrectas += 1
            label_respuestas_incorrectas.configure(text="Respuestas incorrectas: " + str(self.respuestas_incorrectas))

        self.total_ejercicios += 1
        self.porcentaje_respuestas_correctas = self.respuestas_correctas * 100 / self.total_ejercicios
        porcentaje_respuestas_correctas_formateado = round(self.porcentaje_respuestas_correctas, 2)
        label_porcentaje_respuestas_correctas.configure(text="Porcentaje de respuestas correctas: " + str(porcentaje_respuestas_correctas_formateado) + "%")

    def restablecer_color_original(self):
        time.sleep(1)

        for boton in self.botones_intervalos:
            boton.configure(bg="SystemButtonFace", activebackground="SystemButtonFace", fg="SystemButtonText")

    def mostrar_siguiente_intervalo(self):
        time.sleep(1)
        frame_principal = self.master
        frame_principal.iniciar_ejercicio()

    def reproducir_notas(self, nota_1, nota_2):

        numero_midi_nota_1 = self.nota_a_numero(nota_1)
        numero_midi_nota_2 = self.nota_a_numero(nota_2)

        fs = fluidsynth.Synth()
        fs.start(driver='dsound')

        sfid = fs.sfload(r'assets/FluidR3_GM.sf2')
        fs.program_select(0, sfid, 0, 25)
        fs.program_select(1, sfid, 0, 25)

        fs.noteon(0, numero_midi_nota_1, 127)
        fs.noteon(1, numero_midi_nota_2, 127)

        time.sleep(1.0)

        fs.noteoff(0, numero_midi_nota_1)
        fs.noteoff(1, numero_midi_nota_2)

        fs.delete()

    def nota_a_numero(self, nota):

        notas_ordenadas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        indice_nota = notas_ordenadas.index(nota[0])
        octava_nota = nota[1]

        numero = indice_nota + octava_nota * 12 + 12

        return numero
