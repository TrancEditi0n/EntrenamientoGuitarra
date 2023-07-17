import threading
import time
from tkinter import ttk
import pygame
from boton import Boton
from slider import Slider


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
