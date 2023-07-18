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

        self.boton_identificar_notas = Boton(self, "Identificar Notas",
                                             self.boton_identificar_notas_clicked)
        self.boton_identificar_notas.pack()

    def boton_identificar_notas_clicked(self):
        frame_principal = self.master.master

        if not self.ejercicio_iniciado:
            self.ejercicio_iniciado = True
            self.boton_identificar_notas.config(text="Finalizar")
            self.boton_identificar_intervalos.config(state="disabled")
            self.deshabilitar_combos_itervalos()
            frame_principal.crear_frame_ejercicios_diapason_notas()

        else:
            frame_principal.eliminar_frame_ejercicios_diapason()

            self.ejercicio_iniciado = False
            self.boton_identificar_notas.config(text="Identificar Notas")
            self.boton_identificar_intervalos.config(state="enabled")
            self.habilitar_combos_itervalos()


    def boton_identificar_intervalos_clicked(self):
        frame_principal = self.master.master  # Obtener la instancia de FramePrincipalDiapason

        if not self.ejercicio_iniciado:
            self.ejercicio_iniciado = True
            self.boton_identificar_intervalos.config(text="Finalizar")
            self.boton_identificar_notas.config(state="disabled")
            self.deshabilitar_combos_itervalos()

            frame_principal.crear_frame_ejercicios_diapason_intervalos()

        else:

            self.habilitar_combos_itervalos()
            self.boton_identificar_notas.config(state="enabled")

            frame_principal.eliminar_frame_ejercicios_diapason()

            self.ejercicio_iniciado = False
            self.boton_identificar_intervalos.config(text="Identificar Intervalos")

    def deshabilitar_combos_itervalos(self):

        self.combo_distancia_maxima_cuerdas.config(state="disabled")
        self.combo_distancia_maxima_trastes.config(state="disabled")

    def habilitar_combos_itervalos(self):

        self.combo_distancia_maxima_cuerdas.config(state="readonly")
        self.combo_distancia_maxima_trastes.config(state="readonly")
