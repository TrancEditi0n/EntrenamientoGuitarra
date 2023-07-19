import math
import tkinter as tk


class CanvasDiapason(tk.Canvas):
    def __init__(self, master, numero_cuerdas, numero_trastes):
        super().__init__(master)

        self.escala = 2400
        self.posicion_inicial = 50
        self.notas_marcadas = []
        self.r_que_aparece_en_la_nota_mas_grave = None

        # Dibuja los inlays primero para que no aparezcan por encima de las cuerdas

        self.dibujar_inlays(numero_trastes, numero_cuerdas)
        self.dibujar_cuerdas(numero_trastes, numero_cuerdas)
        self.dibujar_trastes(numero_trastes, numero_cuerdas)

        self.ajustar_tamano_ventana()

    def marcar_nota(self, traste, cuerda, es_la_mas_grave):
        distancia_traste = self.escala - (self.escala / math.pow(2, traste / 12))
        distancia_anterior_traste = self.escala - (self.escala / math.pow(2, (traste - 1) / 12))
        x = self.posicion_inicial + (distancia_traste + distancia_anterior_traste) / 2
        y = cuerda * 50
        radio = 15
        fill_color = "red"
        outline_color = "red"
        nota = self.create_oval(x - radio, y - radio, x + radio, y + radio,
                                fill=fill_color, outline=outline_color)

        if es_la_mas_grave:
            # Agrega la letra "R" dentro del óvalo
            texto = "R"
            self.r_que_aparece_en_la_nota_mas_grave = self.create_text(x, y, text=texto, fill="white",
                                                                       font=("Arial", 12), tag=nota)

        self.notas_marcadas.append(nota)

    def borrar_notas(self):
        # Eliminar todos los objetos gráficos de notas en el diapasón
        for nota in self.notas_marcadas:
            self.delete(nota)
        self.notas_marcadas = []

        self.borrar_letra()

    def borrar_letra(self):

        self.delete(self.r_que_aparece_en_la_nota_mas_grave)
        self.r_que_aparece_en_la_nota_mas_grave = None

    def dibujar_cuerdas(self, numero_trastes, numero_cuerdas):

        largo_de_cuerda = self.posicion_inicial + (self.escala - (self.escala / math.pow(2, numero_trastes/12))) + 1

        grosor_maximo = 5
        grosor_minimo = 2

        # Calcula el rango de grosor entre el máximo y el mínimo
        rango_grosor = grosor_maximo - grosor_minimo

        # Calcula el incremento proporcional de grosor entre las cuerdas
        incremento_grosor = rango_grosor / (numero_cuerdas - 1)

        # Dibuja las cuerdas del diapasón
        for i, y in enumerate(range(50, (numero_cuerdas + 1) * 50, 50)):
            grosor_cuerda = grosor_minimo + (i * incremento_grosor)
            self.create_line(self.posicion_inicial - 1, y, largo_de_cuerda, y, width=grosor_cuerda)

    def dibujar_trastes(self, numero_trastes, numero_cuerdas):

        # L_n = L - (L / 2^(n/12)) -> Fórmula para calcular la distancia de los trastes en una guitarra real

        posicion_x = 0

        for i in range(0, numero_trastes + 2, 1):
            self.create_line(self.posicion_inicial + posicion_x, 50, self.posicion_inicial + posicion_x, numero_cuerdas * 50, width=2)
            posicion_x = self.escala - (self.escala / math.pow(2, i/12))

    def dibujar_inlays(self, numero_trastes, numero_cuerdas):

        inlay_trastes = [3, 5, 7, 9, 12, 15, 17, 19, 21, 24]  # Números de trastes donde se dibujarán los inlays

        for traste in inlay_trastes:
            if traste <= numero_trastes:
                distancia_traste = self.escala - (self.escala / math.pow(2, traste / 12))
                distancia_anterior_traste = self.escala - (self.escala / math.pow(2, (traste - 1) / 12))
                x = self.posicion_inicial + (distancia_traste + distancia_anterior_traste) / 2
                y = ((numero_cuerdas + 1) * 50) / 2  # Coordenada y fija para ubicar el inlay en el centro vertical del diapasón
                radio = 10  # Tamaño del radio del inlay
                fill_color = "#CCCCCC"
                outline_color = fill_color

                if traste in (12, 24):
                    radio_1 = radio
                    radio_2 = radio
                    separacion = numero_cuerdas * 9  # Ajusta la separación vertical entre los círculos

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

    def ajustar_tamano_ventana(self):
        coordenadas = self.bbox("all")  # Obtener coordenadas del cuadro delimitador de todos los elementos dibujados
        ancho = coordenadas[2] + 10  # Agregar un margen de 10 píxeles al ancho
        alto = coordenadas[3] + 10  # Agregar un margen de 10 píxeles al alto
        self.config(width=ancho, height=alto)