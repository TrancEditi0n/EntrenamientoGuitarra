import random
from tkinter import ttk
from frame_diapason import FrameDiapason
from frame_ejercicios_diapason import FrameEjerciciosDiapason
from separador_horizontal import SeparadorHorizontal


class FramePrincipalDiapason(ttk.Frame):
    def __init__(self, master, numero_cuerdas, numero_trastes, afinacion):
        super().__init__(master)

        self.notas_ordenadas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.matriz_notas = self.generar_matriz_notas(afinacion, numero_trastes)

        self.intervalo = None
        self.nota_1 = None
        self.nota_2 = None

        self.numero_cuerdas = numero_cuerdas
        self.numero_trastes = numero_trastes

        self.frame_inferior_diapason = None
        self.frame_superior_diapason = FrameDiapason(self, numero_cuerdas, numero_trastes)
        self.separador = SeparadorHorizontal(self)

        self.distancia_maxima_cuerdas = None
        self.distancia_maxima_trastes = None

        self.frame_superior_diapason.pack(fill='both', expand=True)
        self.separador.pack(side='top', fill='x', padx=5, pady=5)



    def crear_frame_ejercicios_diapason_intervalos(self):

        self.frame_inferior_diapason = FrameEjerciciosDiapason(self)
        self.frame_inferior_diapason.pack(fill='both', expand=True)

        self.iniciar_ejercicio()

    def eliminar_frame_ejercicios_diapason_intervalos(self):

        self.frame_inferior_diapason.destroy()

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

        notas_ordenadas_por_mas_grave = self.identificar_nota_mas_grave(cuerda_nota_1, traste_nota_1, cuerda_nota_2, traste_nota_2)

        cuerda_nota_mas_grave = notas_ordenadas_por_mas_grave[0]
        traste_nota_mas_grave = notas_ordenadas_por_mas_grave[1]
        cuerda_nota_mas_aguda = notas_ordenadas_por_mas_grave[2]
        traste_nota_mas_aguda = notas_ordenadas_por_mas_grave[3]

        # Marcar las notas en el diapasón
        self.frame_superior_diapason.frame_canvas.canvas_diapason.marcar_nota(traste_nota_mas_grave, cuerda_nota_mas_grave, True)
        self.frame_superior_diapason.frame_canvas.canvas_diapason.marcar_nota(traste_nota_mas_aguda, cuerda_nota_mas_aguda, False)

        self.intervalo = self.calcular_intervalo(traste_nota_1, cuerda_nota_1, traste_nota_2, cuerda_nota_2)

    def calcular_intervalo(self, traste_nota_1, cuerda_nota_1, traste_nota_2, cuerda_nota_2):

        intervalo = None

        self.nota_1 = self.matriz_notas[cuerda_nota_1 - 1][traste_nota_1 - 1]
        self.nota_2 = self.matriz_notas[cuerda_nota_2 - 1][traste_nota_2 - 1]

        octava_nota_1 = self.nota_1[1]
        octava_nota_2 = self.nota_2[1]

        indice_nota_1 = self.notas_ordenadas.index(self.nota_1[0])
        indice_nota_2 = self.notas_ordenadas.index(self.nota_2[0])

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

    def identificar_nota_mas_grave(self, cuerda_nota_1, traste_nota_1, cuerda_nota_2, traste_nota_2):

        nota_1 = self.matriz_notas[cuerda_nota_1 - 1][traste_nota_1 - 1]
        nota_2 = self.matriz_notas[cuerda_nota_2 - 1][traste_nota_2 - 1]

        octava_nota_1 = nota_1[1]
        octava_nota_2 = nota_2[1]

        indice_nota_1 = self.notas_ordenadas.index(nota_1[0])
        indice_nota_2 = self.notas_ordenadas.index(nota_2[0])

        if octava_nota_1 == octava_nota_2:
            if indice_nota_1 < indice_nota_2:
                return cuerda_nota_1, traste_nota_1, cuerda_nota_2, traste_nota_2

            else:
                return cuerda_nota_2, traste_nota_2, cuerda_nota_1, traste_nota_1

        else:
            if octava_nota_1 < octava_nota_2:
                return cuerda_nota_1, traste_nota_1, cuerda_nota_2, traste_nota_2

            else:
                return cuerda_nota_2, traste_nota_2, cuerda_nota_1, traste_nota_1

    def generar_matriz_notas(self, afinacion_inicial, cantidad_trastes):

        matriz_notas = []
        cantidad_cuerdas = len(afinacion_inicial)

        for cuerda in range(cantidad_cuerdas):
            notas_cuerda = []
            nota, octava = afinacion_inicial[cuerda]
            indice_afinacion = (self.notas_ordenadas.index(nota) + 1) % len(self.notas_ordenadas) # Ajuste para la siguiente nota (en el traste 1)

            if indice_afinacion == 0:
                octava += 1

            for traste in range(cantidad_trastes):
                nota = self.notas_ordenadas[indice_afinacion]
                notas_cuerda.append((nota, octava))

                if indice_afinacion == len(self.notas_ordenadas) - 1:
                    octava += 1

                indice_afinacion = (indice_afinacion + 1) % len(self.notas_ordenadas)

            matriz_notas.append(notas_cuerda)

        return matriz_notas
