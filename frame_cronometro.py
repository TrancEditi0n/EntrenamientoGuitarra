import time
from tkinter import ttk
from boton import Boton


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
