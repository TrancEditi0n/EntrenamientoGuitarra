from tkinter import ttk
from boton import Boton
from combo_box import ComboBox


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
