import random
import threading
import fluidsynth
import time
import tkinter as tk
from tkinter import ttk

import pygame


class EntrenamientoDeGuitarraApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw()

        self.title("Entrenamiento de guitarra")
        self.iconbitmap("assets/electric-guitar_icon.ico")

        window_width = 1000
        window_height = 400

        self.minsize(1000, 400)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(True, True)

        self.frame_principal = FramePrincipal(self)
        self.frame_principal.pack(fill='both', expand=True, padx=10, pady=10)
        self.deiconify()


class FramePrincipal(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frame_inferior = FrameInferior(self)
        self.frame_superior = FrameSuperior(self, self.frame_inferior)
        self.separador = SeparadorHorizontal(self)

        self.frame_superior.pack(fill='both', expand=True)
        self.separador.pack(side='top', fill='x', padx=5, pady=5)
        self.frame_inferior.pack(fill='both', expand=True)


class FrameSuperior(ttk.Frame):
    def __init__(self, master, frame_inferior):
        super().__init__(master)

        self.frame_izquierdo = FrameIzquierdo(self, frame_inferior)
        self.frame_izquierdo.pack(fill='both', expand=True, side='left')

        self.separador_vertical = SeparadorVertical(self)
        self.separador_vertical.pack(side='left', fill='y', padx=5, pady=5)

        self.frame_derecho = FrameDerecho(self)
        self.frame_derecho.pack(fill='both', expand=True, side='right')


class FrameInferior(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.canvas_notas = CanvasNotas(self)
        self.canvas_notas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas_notas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas_notas.configure(yscrollcommand=self.scrollbar.set)


class CanvasNotas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master)

        self.frame_interior = FrameInterior(self)
        self.frame_interior.bind("<Configure>", lambda e: self.configure(scrollregion=self.bbox("all")))

        self.create_window((0, 0), window=self.frame_interior, anchor="nw")


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


class FrameInterior(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)


class FrameDerecho(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.subframe_superior = SubFrameSuperior(self)
        self.subframe_inferior = SubFrameInferior(self)
        self.separador_sub_frames = SeparadorHorizontal(self)

        self.subframe_superior.pack(fill='both', expand=True)
        self.separador_sub_frames.pack(side='top', fill='x', padx=5, pady=5)
        self.subframe_inferior.pack(fill='both', expand=True)


class SubFrameSuperior(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.opciones_cuerdas = [4, 5, 6, 7, 8, 9, 10]
        self.opciones_trastes = [7, 9, 12, 15, 17, 19, 21, 24]

        self.combo_cuerdas = ComboBox(self, self.opciones_cuerdas, 7)
        self.combo_trastes = ComboBox(self, self.opciones_trastes, 24)
        self.label_cuerdas = ttk.Label(self, text="Cantidad de cuerdas:")
        self.label_trastes = ttk.Label(self, text="Cantidad de trastes:")

        self.label_cuerdas.pack()
        self.combo_cuerdas.pack()
        self.label_trastes.pack()
        self.combo_trastes.pack()

        self.boton_mostrar_diapason = Boton(self, "Mostrar Diapasón", self.boton_mostrar_diapason_clicked)
        self.boton_mostrar_diapason.pack(fill="x", padx=5, pady=5, expand=True)

    def boton_mostrar_diapason_clicked(self):

        numero_cuerdas = int(self.combo_cuerdas.get())
        numero_trastes = int(self.combo_trastes.get())

        VentanaDiapason(self, numero_cuerdas, numero_trastes)


class SubFrameInferior(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frame_volumen = FrameVolumenYCronometro(self)
        self.frame_metronomo = FrameMetronomo(self, self.frame_volumen)
        self.frame_volumen.pack(fill='both', expand=True, side='left')
        self.frame_metronomo.pack(fill='both', expand=True, side='right')


class FrameVolumenYCronometro(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_volumen = ttk.Label(self, text="Volumen:")
        self.slider_volumen = Slider(self, 0, 100, 100, 100)

        self.label_volumen.pack(fill='y', padx=5, pady=5)
        self.slider_volumen.pack()

        self.frame_cronometro = FrameCronometro(self)
        self.frame_cronometro.pack()


class FrameCronometro(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.cronometro_encendido = False
        self.tiempo_inicial = 0
        self.tiempo_actual = 0
        self.tiempo_transcurrido = 0

        self.label_cronometro = ttk.Label(self, text="Cronómetro:")
        self.label_cronometro.pack(fill='y', padx=5, pady=5)

        self.label_tiempo = ttk.Label(self, text="00:00:00", font=("Arial", 24))
        self.label_tiempo.pack(fill='y', padx=5, pady=5)

        self.boton_restablecer_cronometro = Boton(self, "Restablecer Cronómetro", self.restablecer_cronometro)
        self.boton_restablecer_cronometro.pack()

    def iniciar_cronometro(self):

        if not self.cronometro_encendido:
            self.cronometro_encendido = True
            self.tiempo_inicial = time.time()
            self.actualizar_cronometro()

    def detener_cronometro(self):
        if self.cronometro_encendido:
            self.cronometro_encendido = False
            self.tiempo_transcurrido += time.time() - self.tiempo_inicial

    def actualizar_cronometro(self):

        if self.cronometro_encendido:
            self.tiempo_actual = int(time.time() - self.tiempo_inicial + self.tiempo_transcurrido)
            tiempo_formateado = time.strftime("%H:%M:%S", time.gmtime(self.tiempo_actual))
            self.label_tiempo.config(text=tiempo_formateado)
            self.after(500, self.actualizar_cronometro)

    def restablecer_cronometro(self):

        self.tiempo_transcurrido = 0
        self.tiempo_inicial = time.time()
        self.label_tiempo.config(text="00:00:00")


class FrameMetronomo(ttk.Frame):
    def __init__(self, master, frame_volumen):
        super().__init__(master)

        self.metronomo_iniciado = False

        def on_slider_move(event):
            value = self.slider_metronomo.get()
            if int(value) != value:
                self.slider_metronomo.set(round(value))
            self.label_bpm.configure(text="BPM: " + str(self.slider_metronomo.get()))

        def iniciar_metronomo_y_cronometro():
            iniciar_metronomo()

            if self.metronomo_iniciado:
                frame_volumen.frame_cronometro.iniciar_cronometro()

        def iniciar_metronomo():

            if not self.metronomo_iniciado:

                self.metronomo_iniciado = True
                pygame.init()
                self.boton_iniciar_metronomo.configure(text="Detener")

                # Configuración de los sonidos del metrónomo
                click_sound = pygame.mixer.Sound("assets/metronomo.mp3")

                def reproducir_metronomo():
                    while self.metronomo_iniciado:
                        bpm = self.slider_metronomo.get()
                        intervalo = (60 / bpm)
                        volumen = frame_volumen.slider_volumen.get()
                        click_sound.set_volume(volumen / 100)
                        click_sound.play()
                        time.sleep(intervalo)

                self.metronomo_thread = threading.Thread(target=reproducir_metronomo)
                self.metronomo_thread.start()

            else:

                self.metronomo_iniciado = False
                frame_volumen.frame_cronometro.detener_cronometro()
                self.boton_iniciar_metronomo.configure(text="Iniciar")
                self.metronomo_thread.join()
                pygame.quit()

        self.label_metronomo = ttk.Label(self, text="Metrónomo:")
        self.label_metronomo.pack(fill='y', padx=5, pady=5)

        self.slider_metronomo = Slider(self, 40, 200, 400, 40)
        self.slider_metronomo.bind("<B1-Motion>", on_slider_move)
        self.slider_metronomo.bind("<ButtonRelease-1>", on_slider_move)
        self.slider_metronomo.pack()

        self.label_bpm = ttk.Label(self, text="BPM: " + str(self.slider_metronomo.get()))
        self.label_bpm.pack(fill='y', padx=5, pady=5)

        self.boton_iniciar_metronomo = Boton(self, "Iniciar Metrónomo", command=iniciar_metronomo_y_cronometro)
        self.boton_iniciar_metronomo.pack()


class SeparadorHorizontal(ttk.Separator):
    def __init__(self, master):
        super().__init__(master, orient='horizontal')


class Slider(ttk.Scale):
    def __init__(self, master, desde, hasta, largo, defecto):
        super().__init__(master, from_=desde, to=hasta, length=largo, orient=tk.HORIZONTAL)
        self.set(defecto)


class SeparadorVertical(ttk.Separator):
    def __init__(self, master):
        super().__init__(master, orient='vertical')


class Boton(ttk.Button):
    def __init__(self, master, text, command):
        super().__init__(master, text=text, command=command)


class VentanaDiapason(tk.Toplevel):
    def __init__(self, master, numero_cuerdas, numero_trastes):
        super().__init__(master)

        self.grab_set()
        self.title("Diapasón de la guitarra")
        self.iconbitmap("assets/diapason.ico")
        self.geometry("1500x900")

        self.frame_principal_diapason = FramePrincipalDiapason(self, numero_cuerdas, numero_trastes)
        self.frame_principal_diapason.pack(fill='both', expand=True, padx=10, pady=10)


class ComboBox(ttk.Combobox):
    def __init__(self, master, opciones, opcion_por_defecto):
        super().__init__(master, state="readonly")
        self['values'] = opciones
        self.set(opcion_por_defecto)


class FramePrincipalDiapason(ttk.Frame):
    def __init__(self, master, numero_cuerdas, numero_trastes):
        super().__init__(master)

        self.intervalo = None
        self.nota_1 = None
        self.nota_2 = None

        self.numero_cuerdas = numero_cuerdas
        self.numero_trastes = numero_trastes

        self.frame_inferior_diapason = FrameEjerciciosDiapason(self)
        self.frame_superior_diapason = FrameDiapason(self, numero_cuerdas, numero_trastes)
        self.separador = SeparadorHorizontal(self)

        self.distancia_maxima_cuerdas = None
        self.distancia_maxima_trastes = None

        self.frame_superior_diapason.pack(fill='both', expand=True)
        self.separador.pack(side='top', fill='x', padx=5, pady=5)
        self.frame_inferior_diapason.pack(fill='both', expand=True)

    def iniciar_ejercicio(self):

        self.distancia_maxima_cuerdas = int(self.frame_superior_diapason.frame_seleccion_ejercicio.combo_distancia_maxima_cuerdas.get())
        self.distancia_maxima_trastes = int(self.frame_superior_diapason.frame_seleccion_ejercicio.combo_distancia_maxima_trastes.get())

        # Activo los botones que me permiten elegir el intervalo

        botones_intervalos = self.frame_inferior_diapason.botones_intervalos

        for boton in botones_intervalos:
            boton.config(state="active")

        # Generar números aleatorios para la cuerda y traste de la primera nota

        traste_nota_1 = random.randint(1, self.numero_trastes)
        cuerda_nota_1 = random.randint(1, self.numero_cuerdas)

        # Calculo la distancia en base a la distancia máxima seleccionada

        distancia_cuerdas = random.randint(-self.distancia_maxima_cuerdas, self.distancia_maxima_cuerdas)
        distancia_trastes = random.randint(-self.distancia_maxima_trastes, self.distancia_maxima_trastes)

        traste_nota_2 = traste_nota_1 + distancia_trastes
        cuerda_nota_2 = cuerda_nota_1 + distancia_cuerdas

        # Verifica si la nueva posición de traste excede los límites del diapasón
        if traste_nota_2 < 1:
            traste_nota_2 = 1
        elif traste_nota_2 > self.numero_trastes:
            traste_nota_2 = self.numero_trastes

        # Verifica si la nueva posición de cuerda excede los límites del diapasón
        if cuerda_nota_2 < 1:
            cuerda_nota_2 = 1
        elif cuerda_nota_2 > self.numero_cuerdas:
            cuerda_nota_2 = self.numero_cuerdas

        # Evito que la segunda nota no sea exactamente igual que la primera, probablemente se pueda hacer
        # de una manera más elegante pero me da paja :P

        while traste_nota_2 == traste_nota_1 and cuerda_nota_2 == cuerda_nota_1:

            distancia_cuerdas = random.randint(-self.distancia_maxima_cuerdas, self.distancia_maxima_cuerdas)
            distancia_trastes = random.randint(-self.distancia_maxima_trastes, self.distancia_maxima_trastes)
            traste_nota_2 = traste_nota_1 + distancia_trastes
            cuerda_nota_2 = cuerda_nota_1 + distancia_cuerdas

            # Verifica si la nueva posición de traste excede los límites del diapasón
            if traste_nota_2 < 1:
                traste_nota_2 = 1
            elif traste_nota_2 > self.numero_trastes:
                traste_nota_2 = self.numero_trastes

            # Verifica si la nueva posición de cuerda excede los límites del diapasón
            if cuerda_nota_2 < 1:
                cuerda_nota_2 = 1
            elif cuerda_nota_2 > self.numero_cuerdas:
                cuerda_nota_2 = self.numero_cuerdas

        # Borra las notas previas en el diapasón
        self.frame_superior_diapason.frame_canvas.canvas_diapason.borrar_notas()

        # Marcar las notas en el diapasón
        self.frame_superior_diapason.frame_canvas.canvas_diapason.marcar_nota(traste_nota_1, cuerda_nota_1)
        self.frame_superior_diapason.frame_canvas.canvas_diapason.marcar_nota(traste_nota_2, cuerda_nota_2)

        self.intervalo = self.calcular_intervalo(traste_nota_1, cuerda_nota_1, traste_nota_2, cuerda_nota_2)

    def calcular_intervalo(self, traste_nota_1, cuerda_nota_1, traste_nota_2, cuerda_nota_2):

        intervalo = None

        notas_ordenadas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        matriz_notas = [[("F", 4), ("F#", 4), ("G", 4), ("G#", 4), ("A", 4), ("A#", 4), ("B", 4), ("C", 5), ("C#", 5), ("D", 5), ("D#", 5), ("E", 5), ("F", 5), ("F#", 5), ("G", 5), ("G#", 5), ("A", 5), ("A#", 5), ("B", 5), ("C", 6), ("C#", 6), ("D", 6), ("D#", 6), ("E", 6)],
                        [("C", 4), ("C#", 4), ("D", 4), ("D#", 4), ("E", 4), ("F", 4), ("F#", 4), ("G", 4), ("G#", 4), ("A", 4), ("A#", 4), ("B", 4), ("C", 5), ("C#", 5), ("D", 5), ("D#", 5), ("E", 5), ("F", 5), ("F#", 5), ("G", 5), ("G#", 5), ("A", 5), ("A#", 5), ("B", 5)],
                        [("G#", 3), ("A", 3), ("A#", 3), ("B", 3), ("C", 4), ("C#", 4), ("D", 4), ("D#", 4), ("E", 4), ("F", 4), ("F#", 4), ("G", 4), ("G#", 4), ("A", 4), ("A#", 4), ("B", 4), ("C", 5), ("C#", 5), ("D", 5), ("D#", 5), ("E", 5), ("F", 5), ("F#", 5), ("G", 5)],
                        [("D#", 3), ("E", 3), ("F", 3), ("F#", 3), ("G", 3), ("G#", 3), ("A", 3), ("A#", 3), ("B", 3), ("C", 4), ("C#", 4), ("D", 4), ("D#", 4), ("E", 4), ("F", 4), ("F#", 4), ("G", 4), ("G#", 4), ("A", 4), ("A#", 4), ("B", 4), ("C", 5), ("C#", 5), ("D", 5)],
                        [("A#", 2), ("B", 2), ("C", 3), ("C#", 3), ("D", 3), ("D#", 3), ("E", 3), ("F", 3), ("F#", 3), ("G", 3), ("G#", 3), ("A", 3), ("A#", 3), ("B", 3), ("C", 4), ("C#", 4), ("D", 4), ("D#", 4), ("E", 4), ("F", 4), ("F#", 4), ("G", 4), ("G#", 4), ("A", 4)],
                        [("F", 2), ("F#", 2), ("G", 2), ("G#", 2), ("A", 2), ("A#", 2), ("B", 2), ("C", 3), ("C#", 3), ("D", 3), ("D#", 3), ("E", 3), ("F", 3), ("F#", 3), ("G", 3), ("G#", 3), ("A", 3), ("A#", 3), ("B", 3), ("C", 4), ("C#", 4), ("D", 4), ("D#", 4), ("E", 4)],
                        [("C", 2), ("C#", 2), ("D", 2), ("D#", 2), ("E", 2), ("F", 2), ("F#", 2), ("G", 2), ("G#", 2), ("A", 2), ("A#", 2), ("B", 2), ("C", 3), ("C#", 3), ("D", 3), ("D#", 3), ("E", 3), ("F", 3), ("F#", 3), ("G", 3), ("G#", 3), ("A", 3), ("A#", 3), ("B", 3)]]

        self.nota_1 = matriz_notas[cuerda_nota_1 - 1][traste_nota_1 - 1]
        self.nota_2 = matriz_notas[cuerda_nota_2 - 1][traste_nota_2 - 1]

        octava_nota_1 = self.nota_1[1]
        octava_nota_2 = self.nota_2[1]

        indice_nota_1 = notas_ordenadas.index(self.nota_1[0])
        indice_nota_2 = notas_ordenadas.index(self.nota_2[0])

        distancia_en_semitonos = 0

        if octava_nota_1 == octava_nota_2:
            distancia_en_semitonos = abs(indice_nota_1 - indice_nota_2)
        else:

            # Identifico la nota más grave y la más aguda
            if octava_nota_1 < octava_nota_2:
                indice_nota_mas_grave = indice_nota_1
                indice_nota_mas_aguda = indice_nota_2
            else:
                indice_nota_mas_grave = indice_nota_2
                indice_nota_mas_aguda = indice_nota_1

            octavas_de_diferencia = abs(octava_nota_1 - octava_nota_2)
            distancia_en_semitonos += 12 * octavas_de_diferencia

            if indice_nota_mas_grave < indice_nota_mas_aguda:
                distancia_en_semitonos += abs(indice_nota_1 - indice_nota_2)
            else:
                distancia_en_semitonos -= abs(indice_nota_1 - indice_nota_2)

        match distancia_en_semitonos % 12:

            case 0:
                if distancia_en_semitonos == 0:
                    intervalo = "Unísono"
                else:
                    intervalo = "Octava"
            case 1:
                intervalo = "Segunda Menor"
            case 2:
                intervalo = "Segunda Mayor"
            case 3:
                intervalo = "Tercera Menor"
            case 4:
                intervalo = "Tercera Mayor"
            case 5:
                intervalo = "Cuarta Justa"
            case 6:
                intervalo = "Tritono"
            case 7:
                intervalo = "Quinta Justa"
            case 8:
                intervalo = "Sexta Menor"
            case 9:
                intervalo = "Sexta Mayor"
            case 10:
                intervalo = "Séptima Menor"
            case 11:
                intervalo = "Séptima Mayor"

        return intervalo


class FrameDiapason(ttk.Frame):
    def __init__(self, master, numero_cuerdas, numero_trastes):
        super().__init__(master)

        self.frame_canvas = FrameCanvas(self, numero_cuerdas, numero_trastes)
        self.frame_seleccion_ejercicio = FrameSeleccionEjercicio(self)

        self.frame_canvas.pack()
        self.frame_seleccion_ejercicio.pack(fill='both', expand=True)


class FrameCanvas(ttk.Frame):
    def __init__(self, master, numero_cuerdas, numero_trastes):
        super().__init__(master)

        self.canvas_diapason = CanvasDiapason(self, numero_cuerdas, numero_trastes)
        self.canvas_diapason.pack()


class FrameSeleccionEjercicio(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.ejercicio_iniciado = False

        frame_principal_diapason = self.master.master

        self.label_ejercicios = ttk.Label(self, text="Selección de ejercicios:")
        self.label_ejercicios.pack()

        self.boton_identificar_intervalos = Boton(self, "Identificar Intervalos",
                                                  self.boton_identificar_intervalos_clicked)
        self.boton_identificar_intervalos.pack()

        self.opciones_distancia_maxima_cuerdas = list(range(1, frame_principal_diapason.numero_cuerdas))
        self.opciones_distancia_maxima_trastes = list(range(1, frame_principal_diapason.numero_trastes))

        self.combo_distancia_maxima_cuerdas = ComboBox(self, self.opciones_distancia_maxima_cuerdas, 3)
        self.combo_distancia_maxima_trastes = ComboBox(self, self.opciones_distancia_maxima_trastes, 4)
        self.label_distancia_cuerdas = ttk.Label(self, text="Distancia máxima entre cuerdas:")
        self.label_distancia_trastes = ttk.Label(self, text="Distancia máxima entre trastes:")

        self.label_distancia_cuerdas.pack()
        self.combo_distancia_maxima_cuerdas.pack()
        self.label_distancia_trastes.pack()
        self.combo_distancia_maxima_trastes.pack()

        self.label_respuestas_correctas = ttk.Label(self, text="Respuestas correctas: 0")
        self.label_respuestas_incorrectas = ttk.Label(self, text="Respuestas Incorrectas: 0")
        self.label_porcentaje_respuestas_correctas = ttk.Label(self, text="Porcentaje de respuestas correctas: 0%")

        self.label_respuestas_correctas.pack()
        self.label_respuestas_incorrectas.pack()
        self.label_porcentaje_respuestas_correctas.pack()

    def boton_identificar_intervalos_clicked(self):

        frame_principal = self.master.master  # Obtener la instancia de FramePrincipalDiapason

        if not self.ejercicio_iniciado:
            self.ejercicio_iniciado = True
            self.boton_identificar_intervalos.config(text="Finalizar")

            self.combo_distancia_maxima_cuerdas.config(state="disabled")
            self.combo_distancia_maxima_trastes.config(state="disabled")

            frame_principal.iniciar_ejercicio()

        else:

            self.combo_distancia_maxima_cuerdas.config(state="readonly")
            self.combo_distancia_maxima_trastes.config(state="readonly")

            # Deshabilito los botones de intervalos

            botones_intervalos = frame_principal.frame_inferior_diapason.botones_intervalos

            for boton in botones_intervalos:
                boton.config(state="disabled")

            self.ejercicio_iniciado = False
            self.boton_identificar_intervalos.config(text="Identificar Intervalos")


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
        fs.start(driver='dsound')  # use DirectSound driver

        sfid = fs.sfload(r'assets/FluidR3_GM.sf2')  # replace path as needed
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


class CanvasDiapason(tk.Canvas):
    def __init__(self, master, numero_cuerdas, numero_trastes):
        super().__init__(master)

        self.config(width=1500, height=400)
        self.notas_marcadas = []

        # Dibuja los inlays primero para que no aparezcan por encima de las cuerdas

        self.dibujar_inlays(numero_trastes, numero_cuerdas)
        self.dibujar_cuerdas(numero_trastes, numero_cuerdas)
        self.dibujar_trastes(numero_trastes, numero_cuerdas)

    def dibujar_inlays(self, numero_trastes, numero_cuerdas):

        inlay_trastes = [3, 5, 7, 9, 12, 15, 17, 19, 21, 24]  # Números de trastes donde se dibujarán los inlays

        for traste in inlay_trastes:
            if traste <= numero_trastes:
                x = (traste + 0.5) * 50  # Calcula la coordenada x del centro del inlay
                y = ((numero_cuerdas + 1) * 50) / 2  # Coordenada y fija para ubicar el inlay en
                # el centro vertical del diapasón
                radio = 10  # Tamaño del radio del inlay
                fill_color = "#CCCCCC"
                outline_color = fill_color

                if traste in (12, 24):
                    radio_1 = radio
                    radio_2 = radio
                    separacion = numero_cuerdas * 9  # Ajusta la separación entre los círculos
                    # Por qué * 9? No hay por qué

                    y1 = y - separacion - radio_1
                    y2 = y + separacion + radio_2

                    self.create_oval(x - radio_1, y1 - radio_1, x + radio_1, y1 + radio_1,
                                     fill=fill_color, outline=outline_color)
                    self.create_oval(x - radio_2, y2 - radio_2, x + radio_2, y2 + radio_2,
                                     fill=fill_color, outline=outline_color)
                else:
                    self.create_oval(x - radio, y - radio, x + radio, y + radio,
                                     fill=fill_color, outline=outline_color)
            else:
                break

    def marcar_nota(self, traste, cuerda):
        x = (traste + 0.5) * 50
        y = cuerda * 50
        radio = 15
        fill_color = "red"
        outline_color = "red"
        nota = self.create_oval(x - radio, y - radio, x + radio, y + radio,
                         fill=fill_color, outline=outline_color)
        self.notas_marcadas.append(nota)

    def borrar_notas(self):
        # Eliminar todos los objetos gráficos de notas en el diapasón
        for nota in self.notas_marcadas:
            self.delete(nota)
        self.notas_marcadas = []

    def dibujar_cuerdas(self, numero_trastes, numero_cuerdas):

        grosor_maximo = 5
        grosor_minimo = 2

        # Calcula el rango de grosor entre el máximo y el mínimo
        rango_grosor = grosor_maximo - grosor_minimo

        # Calcula el incremento proporcional de grosor entre las cuerdas
        incremento_grosor = rango_grosor / (numero_cuerdas - 1)

        # Dibuja las cuerdas del diapasón
        for i, y in enumerate(range(50, (numero_cuerdas + 1) * 50, 50)):
            grosor_cuerda = grosor_minimo + (i * incremento_grosor)
            self.create_line(49, y, (numero_trastes + 1) * 50 + 1, y, width=grosor_cuerda)

    def dibujar_trastes(self, numero_trastes, numero_cuerdas):

        for x in range(50, (numero_trastes + 1) * 50 + 1, 50):
            self.create_line(x, 50, x, numero_cuerdas * 50, width=2)


if __name__ == "__main__":
    AplicacionPrincipal = EntrenamientoDeGuitarraApp()
    AplicacionPrincipal.mainloop()
