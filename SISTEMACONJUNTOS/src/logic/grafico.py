import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame
from itertools import combinations

def mostrar_graficos(conjuntos, etiquetas, ventana):
    from SISTEMACONJUNTOS.src.logic.agrupador import agrupar_conjuntos

    grupos = agrupar_conjuntos(conjuntos)
    index = 0

    # Crear un marco para organizar los gráficos
    marco = Frame(ventana)
    marco.pack(expand=True, fill='both')

    def calcular_intersecciones_con_coordenadas(conj, grupo):
        intersecciones = {}
        num_conj = len(conj)
        coordenadas_intersecciones = {}
        elementos_por_region = {}

        # Definir coordenadas específicas según el número de conjuntos
        if grupo == 2:
            coordenadas_intersecciones = {
                (0,): (-2, 0), (1,): (2, 0),
                (0, 1): (0, 0)
            }
        elif grupo == 3:
            coordenadas_intersecciones = {
                (0,): (-4, 3), (1,): (2, 3), (2,): (-2, -2),
                (0, 1): (-0.6, 3), (0, 2): (-2, 0), (1, 2): (1, 0),
                (0, 1, 2): (-0.8, 1)
            }
        elif grupo == 4:
            coordenadas_intersecciones = {
                (0,): (-4, 3), (1,): (2, 3), (2,): (-4, -3), (3,): (2, -3),
                (0, 1): (-1, 3), (0, 2): (-4, 0), (0, 3): (-1, 0),
                (1, 2): (1, 3), (1, 3): (2, 0), (2, 3): (-1, -3),
                (0, 1, 2): (-2, 1), (0, 1, 3): (0, 1),
                (0, 2, 3): (-2, -1), (1, 2, 3): (0, -1),
                (0, 1, 2, 3): (0, 0)
            }

        conjuntos_set = [set(c) for c in conj]

        # Calcular elementos exclusivos de cada conjunto
        for i in range(num_conj):
            otros_conjuntos = [conjuntos_set[j] for j in range(num_conj) if j != i]
            elementos_exclusivos = conjuntos_set[i].difference(*otros_conjuntos)
            elementos_por_region[(i,)] = elementos_exclusivos

        # Calcular las intersecciones
        for i in range(2, num_conj + 1):
            for combinacion_indices in combinations(range(num_conj), i):
                conjuntos_intersecar = [conjuntos_set[j] for j in combinacion_indices]
                interseccion = set.intersection(*conjuntos_intersecar)

                # Restar los elementos que ya están en intersecciones mayores
                for j in range(i + 1, num_conj + 1):
                    for combinacion_mayor_indices in combinations(range(num_conj), j):
                        if all(idx in combinacion_mayor_indices for idx in combinacion_indices):
                            conjuntos_mayor = [conjuntos_set[k] for k in combinacion_mayor_indices]
                            interseccion -= set.intersection(*conjuntos_mayor)

                if interseccion:
                    elementos_por_region[combinacion_indices] = interseccion

        return elementos_por_region, coordenadas_intersecciones

    def ajustar_texto(ax, texto, x, y, max_width=1.5, max_lines=3, fontsize=8, **kwargs):
        words = texto.split(', ')
        lines = []
        current_line = []
        for word in words:
            test_line = current_line + [word]
            text_obj = ax.text(x, y, ', '.join(test_line), fontsize=fontsize, ha='center', va='center', **kwargs)
            bbox = text_obj.get_window_extent(renderer=ax.figure.canvas.get_renderer())
            bbox_width_norm = bbox.width / fig.dpi / (ax.get_xlim()[1] - ax.get_xlim()[0])
            text_obj.remove() # Eliminar el objeto de texto de prueba
            if bbox_width_norm > max_width and current_line:
                lines.append(', '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        if current_line:
            lines.append(', '.join(current_line))

        y_offset = 0
        for line in lines[:max_lines]:
            ax.text(x, y + y_offset, line, fontsize=fontsize, ha='center', va='center', **kwargs)
            y_offset -= 0.2 # Ajustar el espaciado entre líneas
        if len(lines) > max_lines:
            ax.text(x, y + y_offset - 0.2, "...", fontsize=fontsize, ha='center', va='center', **kwargs)

    for num_grupo, grupo in enumerate(grupos):
        # Ajuste dinámico del tamaño del gráfico según la cantidad total de gráficos
        ancho_figura = 6 if len(grupos) == 1 else 5 if len(grupos) == 2 else 4
        alto_figura = 6

        # Crear el gráfico para el grupo actual de conjuntos
        fig, ax = plt.subplots(figsize=(ancho_figura, alto_figura))
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect('equal')
        ax.axis('on')

        # Función para dibujar un círculo
        def dibujar_circulo(ax, x, y, r, color, label):
            circulo = plt.Circle((x, y), r, color=color, alpha=0.4, label=label)
            ax.add_artist(circulo)

        # Colores para los conjuntos
        colores = ['red', 'blue', 'green', 'yellow']

        # Coordenadas para los gráficos (hasta 4 conjuntos)
        coordenadas = [(-1.5, 1.5), (1.5, 1.5), (-1.5, -1.5), (1.5, -1.5)]

        # Ajuste de coordenadas para 3 conjuntos (2 arriba y 1 centrado abajo)
        if grupo == 3:
            coordenadas = [(-1.5, 1.5), (1.5, 1.5), (0, -1.5)]

        # Dibujar los conjuntos y sus etiquetas
        conjuntos_actuales = [set(conjuntos[index + i]) for i in range(grupo)]
        elementos_por_region, coords_inter = calcular_intersecciones_con_coordenadas(conjuntos_actuales, grupo)

        for i in range(grupo):
            dibujar_circulo(ax, *coordenadas[i], 3, colores[i], etiquetas[index + i])

        # Mostrar los elementos en sus respectivas regiones con ajuste de texto
        for region, elementos in elementos_por_region.items():
            if elementos:
                coords = coords_inter.get(region)
                if coords:
                    texto = ", ".join(map(str, elementos))
                    ajustar_texto(ax, texto, coords[0], coords[1], fontsize=8,
                                  bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

        plt.title(f"Diagrama de Venn para {grupo} conjuntos")
        plt.legend(loc='upper right')

        # Convertir el gráfico a un canvas de Tkinter y agregarlo a la ventana
        canvas = FigureCanvasTkAgg(fig, master=marco)

        # Posicionamiento de los gráficos según la cantidad
        if len(grupos) == 1:
            canvas.get_tk_widget().pack(expand=True, fill='both')
        elif len(grupos) == 2:
            canvas.get_tk_widget().grid(row=0, column=num_grupo, padx=20, pady=20, sticky='nsew')
        elif len(grupos) == 3:
            canvas.get_tk_widget().grid(row=0, column=num_grupo, padx=20, pady=20, sticky='nsew')

        canvas.draw()
        index += grupo

    # Ajustar el tamaño de las columnas para que se distribuyan uniformemente
    for col in range(len(grupos)):
        marco.grid_columnconfigure(col, weight=1)