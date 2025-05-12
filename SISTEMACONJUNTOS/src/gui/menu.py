import tkinter as tk
from tkinter import ttk, messagebox
from SISTEMACONJUNTOS.src.logic.grafico import mostrar_graficos

class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Proyecto de Conjuntos")
        self.root.geometry("800x600")
        self.root.configure(bg='#2E3440') # Establecer el color de fondo de la ventana principal

        # --- Estilos ttk ---
        self.style = ttk.Style(self.root)
        self.style.theme_use('alt') # Un tema base limpio

        # --- Configuración de Estilos Personalizados ---
        self.style.configure('TLabel', background='#434C5E', foreground='#E5E9F0', font=('Segoe UI', 12), padding=8)
        self.style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), background='#2E3440', foreground='#E5E9F0', padding=15)
        self.style.configure('TButton',
                             background='#81A1C1',
                             foreground='#2E3440',
                             font=('Segoe UI', 12, 'bold'),
                             padding=10)
        self.style.map('TButton',
                         background=[('active', '#5E81AC')], # Tono más oscuro al hacer clic
                         foreground=[('active', '#E5E9F0')])
        self.style.configure('TEntry',
                             background='#434C5E',
                             foreground='#000000',
                             font=('Segoe UI', 12),
                             padding=5,
                             insertcolor='#E5E9F0') # Color del cursor
        self.style.configure('TCombobox',
                             background='#434C5E',
                             foreground='#000000',
                             font=('Segoe UI', 12),
                             padding=5)
        self.style.configure('TSpinbox',
                             background='#434C5E',
                             foreground='#000000',
                             font=('Segoe UI', 12),
                             padding=5)
        self.style.configure('TFrame', background='#2E3440') # Fondo para los frames contenedores

        # --- Estilo para botones deshabilitados ---
        self.style.configure('Disabled.TButton',
                             background='#3B4252',
                             foreground='#8FBCBB', # Un tono más claro para indicar deshabilitado
                             font=('Segoe UI', 12),
                             padding=10)

        self.conjuntos = {}
        self.btn_editar = None
        self.btn_operacion = None
        self.btn_mostrar = None
        self.conjuntos_data = {}
        self.entry_elementos = {}
        self.frame_conjuntos = {}
        self.available_letters = [chr(i) for i in range(65, 75)]
        self.top_input = None
        self.cantidad_var = tk.IntVar(value=2)
        self.spinbox_cantidad = None
        self.btn_crear_campos = None
        self.btn_agregar = None
        self.btn_guardar = None
        self.create_widgets()

    def _ordenar_elementos(self, event):
        entry_widget = event.widget
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]

        def sort_key(item):
            try:
                num = float(item)
                if num == int(num):
                    return (0, int(num), item)
                else:
                    return (1, num, item)
            except ValueError:
                return (2, item)

        elementos_unicos_ordenados = sorted(list(set(elementos_lista)), key=sort_key)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ", ".join(elementos_unicos_ordenados))

    def create_widgets(self):
        label = ttk.Label(self.root, text="Menú Principal", style='Title.TLabel')
        label.pack(pady=30)

        btn_ingresar = ttk.Button(self.root, text="Ingresar Conjuntos", command=self.open_input_window)
        btn_ingresar.pack(pady=15, padx=20, fill='x')

        btn_editar = ttk.Button(self.root, text="Editar Conjuntos", command=self.open_edit_window, state=tk.DISABLED)
        btn_editar.pack(pady=15, padx=20, fill='x')
        self.btn_editar = btn_editar

        btn_operacion = ttk.Button(self.root, text="Realizar Operación", command=self.open_operation_window, state=tk.DISABLED)
        btn_operacion.pack(pady=15, padx=20, fill='x')
        self.btn_operacion = btn_operacion

        btn_mostrar = ttk.Button(self.root, text="Mostrar Diagramas de Venn", command=self.mostrar_diagrama, state=tk.DISABLED)
        btn_mostrar.pack(pady=15, padx=20, fill='x')
        self.btn_mostrar = btn_mostrar

        btn_salir = ttk.Button(self.root, text="Salir", command=self.root.quit)
        btn_salir.pack(pady=15, padx=20, fill='x')

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

    def open_input_window(self):

        self.top_input = tk.Toplevel(self.root, bg='#2E3440') # Fondo de la ventana secundaria
        self.top_input.title("Ingresar Cantidad de Conjuntos")
        self.top_input.grab_set()
        ttk.Label(self.top_input, text="Seleccione la cantidad de conjuntos (2-10):", style='TLabel').pack(pady=10)
        self.cantidad_var = tk.IntVar(value=2)
        spinbox_cantidad = ttk.Spinbox(self.top_input, from_=2, to=10, textvariable=self.cantidad_var, width=5)
        spinbox_cantidad.pack(pady=5)
        self.spinbox_cantidad = spinbox_cantidad
        btn_crear_campos = ttk.Button(self.top_input, text="Crear Campos de Conjuntos", command=self._crear_campos_despues_cantidad)
        btn_crear_campos.pack(pady=10)
        self.btn_crear_campos = btn_crear_campos
        self.root.wait_window(self.top_input)
        
    def _crear_campos_despues_cantidad(self):
        cantidad = self.cantidad_var.get()
        if not 2 <= cantidad <= 10:
            messagebox.showerror("Error", "La cantidad de conjuntos debe estar entre 2 y 10.")
            return

        if self.top_input:
            self.top_input.destroy()
            self.top_input = None

        # --- Nueva ventana para ingresar el Universo ---
        top_universo_inicial = tk.Toplevel(self.root, bg='#2E3440')
        top_universo_inicial.title("Ingresar Conjunto Universo")
        top_universo_inicial.grab_set()

        ttk.Label(top_universo_inicial, text="Ingrese los elementos del Conjunto Universo (separados por comas):", style='TLabel').pack(pady=10)
        entry_universo_inicial = ttk.Entry(top_universo_inicial, width=50)
        entry_universo_inicial.pack(pady=5, padx=10)
        btn_guardar_universo_inicial = ttk.Button(top_universo_inicial, text="Guardar Universo",
                                                 command=lambda: self._guardar_universo_inicial(entry_universo_inicial,
                                                                                                  top_universo_inicial,
                                                                                                  cantidad))
        btn_guardar_universo_inicial.pack(pady=10)
        self.root.wait_window(top_universo_inicial)

    def _guardar_universo_inicial(self, entry, window, cantidad_conjuntos):
        elementos_str = entry.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
        self.universo = set(elementos_lista)  # Guardar como elementos individuales
        print("Universo guardado:", self.universo)
        window.destroy()
        self._crear_campos_conjuntos(cantidad_conjuntos)
        
    def _crear_campos_conjuntos(self, cantidad):
        self.top_input = tk.Toplevel(self.root, bg='#2E3440')
        self.top_input.title("Ingresar Datos de Conjuntos")
        self.top_input.grab_set()

        universo_texto = ""
        if self.universo:
            universo_texto = ", ".join(sorted(list(self.universo)))

        universo_label = ttk.Label(self.top_input, text=f"Conjunto Universo: { {universo_texto} }", style='TLabel')
        universo_label.pack(pady=10)

        self.frame_conjuntos = {}
        self.conjuntos_data = {}

        for i in range(cantidad):
            frame_conjunto = ttk.Frame(self.top_input)
            frame_conjunto.pack(pady=5, padx=10, fill='x')

            letra_var = tk.StringVar()
            available = self._obtener_letras_disponibles()
            default_letter = available[0] if available else (self.available_letters[i] if i < len(self.available_letters) else "")
            letra_var.set(default_letter)

            combo_letras = ttk.Combobox(frame_conjunto, textvariable=letra_var, values=sorted(self.available_letters), width=3)
            combo_letras.pack(side='left')
            combo_letras.bind("<<ComboboxSelected>>", self._validar_letras_duplicadas)
            combo_letras.bind("<FocusOut>", self._validar_letras_duplicadas)

            ttk.Label(frame_conjunto, text=" = {", width=4, anchor='w').pack(side='left')

            entry = ttk.Entry(frame_conjunto, width=40)
            entry.pack(side='left', expand=True)
            entry.bind("<FocusOut>", self._validar_elementos_en_universo) # Validar al salir del campo
            entry.bind("<FocusOut>", self._ordenar_elementos)
            entry.bind("<Return>", self._ordenar_elementos)
            entry.bind("<Return>", self._validar_elementos_en_universo) # Validar al presionar Enter
            entry.bind("<FocusOut>", self._validar_cantidad_elementos) # Validar cantidad al salir
            entry.bind("<Return>", self._validar_cantidad_elementos) # Validar cantidad al presionar Enter

            ttk.Label(frame_conjunto, text="}").pack(side='left')

            self.frame_conjuntos[frame_conjunto] = (letra_var, entry, combo_letras)
            self.conjuntos_data[letra_var.get()] = set()

        self.btn_guardar = ttk.Button(self.top_input, text="Guardar Conjuntos", command=self.guardar_conjuntos, state=tk.DISABLED)
        self.btn_guardar.pack(pady=10)
        self._actualizar_boton_guardar()
        self.root.wait_window(self.top_input)

    def _obtener_letras_disponibles(self):
        used_letters = set([v[0].get() for _, v in self.frame_conjuntos.items()])
        return sorted([letter for letter in self.available_letters if letter not in used_letters])

    def _validar_letras_duplicadas(self, event=None):
        letras = [v[0].get().strip() for _, v in self.frame_conjuntos.items()]
        letras_validas = [l for l in letras if l]
        duplicados = len(letras_validas) != len(set(letras_validas))
        self._actualizar_boton_guardar(duplicados) # Pasar el estado de duplicados a la función de actualización

    def _actualizar_boton_guardar(self, hay_duplicados=False):
        num_conjuntos = len(self.frame_conjuntos)
        letras = [v[0].get().strip() for _, v in self.frame_conjuntos.items()]
        letras_validas = [l for l in letras if l]
        suficientes_conjuntos = num_conjuntos >= 2

        if suficientes_conjuntos and not hay_duplicados and all(letras_validas):
            self.btn_guardar.config(state=tk.NORMAL)
        else:
            self.btn_guardar.config(state=tk.DISABLED)

    def _ordenar_elementos(self, event):
        entry_widget = event.widget
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
        elementos_unicos = sorted(list(set(elementos_lista)))
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ", ".join(elementos_unicos))
   
    def _validar_elementos_en_universo(self, event):
        entry_widget = event.widget
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
        elementos_invalidos = set(elementos_lista) - self.universo
        if elementos_invalidos:
            messagebox.showerror("Error", f"Los siguientes elementos no están en el Universo: {', '.join(sorted(list(elementos_invalidos)))}")
            entry_widget.delete(0, tk.END) # Limpiar el campo para que el usuario corrija
            entry_widget.focus_set()

    def _validar_elementos_en_universo_editar(self, event, letra):
        entry_widget = self.entry_editar[letra]
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
        elementos_invalidos = set(elementos_lista) - self.universo
        if elementos_invalidos:
            messagebox.showerror("Error", f"El Conjunto {letra} contiene elementos no presentes en el Universo: {', '.join(sorted(list(elementos_invalidos)))}")
            # No limpiar el campo aquí para permitir la corrección en la edición

    def guardar_conjuntos(self):
        errores = {}
        self.conjuntos = {}
        for frame, (letra_var, entry, _) in self.frame_conjuntos.items():
            letra = letra_var.get()
            elementos_str = entry.get()
            elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
            elementos_unicos = set(elementos_lista)

            if len(elementos_unicos) > 15:
                errores[letra] = f"El Conjunto {letra} excede el máximo de 15 elementos ({len(elementos_unicos)})."

            elementos_invalidos = elementos_unicos - self.universo
            if elementos_invalidos:
                if letra not in errores:
                    errores[letra] = ""
                errores[letra] += f" Contiene elementos no presentes en el Universo: {', '.join(sorted(list(elementos_invalidos)))}."
                errores[letra] = errores[letra].lstrip()

            if len(elementos_lista) != len(elementos_unicos) and elementos_lista:
                duplicados = [elem for elem in elementos_lista if elementos_lista.count(elem) > 1]
                if letra not in errores:
                    errores[letra] = ""
                errores[letra] += f" Se encontraron duplicados: {', '.join(sorted(list(set(duplicados))))}."
                errores[letra] = errores[letra].lstrip()

            self.conjuntos[letra] = sorted(list(elementos_unicos))

        if errores:
            mensaje_error = "Se encontraron los siguientes errores:\n"
            for letra, error in errores.items():
                mensaje_error += f"{letra}: {error}\n"
            tk.messagebox.showerror("Errores al Guardar", mensaje_error)
        else:
            print("Guardando conjuntos:", self.conjuntos)
            if self.top_input:
                self.top_input.destroy()
            self.btn_editar.config(state=tk.NORMAL)
            self.btn_operacion.config(state=tk.NORMAL)
            self.btn_mostrar.config(state=tk.NORMAL)

    def _validar_cantidad_elementos(self, event):
        entry_widget = event.widget
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
        if len(set(elementos_lista)) > 15:
            messagebox.showerror("Error", "Cada conjunto no puede tener más de 15 elementos.")
            entry_widget.delete(0, tk.END) # Limpiar el campo

    def _validar_cantidad_elementos_editar(self, event, letra):
        entry_widget = self.entry_editar[letra]
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
        if len(set(elementos_lista)) > 15:
            messagebox.showerror("Error", f"El Conjunto {letra} no puede tener más de 15 elementos.")
            # No limpiar el campo en la edición para permitir la corrección
    
    def mostrar_diagrama(self):
        if not self.conjuntos:
            tk.messagebox.showerror("Error", "Por favor, ingrese los conjuntos primero.")
            return

        ventana_graficos = tk.Toplevel(self.root)
        ventana_graficos.title("Diagramas de Venn")
        ventana_graficos.attributes('-fullscreen', True)

        marco_principal = tk.Frame(ventana_graficos)
        marco_principal.pack(expand=True, fill='both')

        marco_graficos = tk.Frame(marco_principal)
        marco_graficos.pack(side=tk.TOP, expand=True, fill='both')

        marco_descripcion = tk.Frame(marco_principal)
        marco_descripcion.pack(side=tk.BOTTOM, fill='x', pady=10)

        tk.Label(marco_descripcion, text="Descripción de Conjuntos:", font=("Arial", 12, "bold")).pack(pady=5)

        texto_descripcion = tk.Text(marco_descripcion, height=len(self.conjuntos) + 1)
        texto_descripcion.pack(fill='x', padx=10)
        texto_descripcion.config(state=tk.DISABLED)

        descripcion_texto = ""
        for letra, conjunto in self.conjuntos.items():
            descripcion_texto += f"Conjunto {letra}= {', '.join(map(str, conjunto))}\n"

        texto_descripcion.config(state=tk.NORMAL)
        texto_descripcion.insert(tk.END, descripcion_texto)
        texto_descripcion.config(state=tk.DISABLED)

        tk.Button(ventana_graficos, text="Cerrar", command=ventana_graficos.destroy, font=("Arial", 14)).pack(pady=10)

        # Convertir el diccionario de conjuntos a listas ordenadas para la función mostrar_graficos
        conjuntos_lista = [self.conjuntos[letra] for letra in sorted(self.conjuntos.keys())]
        etiquetas_lista = sorted(self.conjuntos.keys())
        mostrar_graficos(conjuntos_lista, etiquetas_lista, marco_graficos)
        
    def run(self):
        self.root.mainloop()

    def open_operation_window(self):
        if not self.conjuntos:
            tk.messagebox.showerror("Error", "Por favor, ingrese los conjuntos primero.")
            return

        top_operacion = tk.Toplevel(self.root, bg='#2E3440') # Fondo de la ventana
        top_operacion.title("Realizar Operación")

        letras_conjuntos = sorted(list(self.conjuntos.keys()))
        operaciones = ["Unión", "Intersección", "Diferencia (A-B)", "Diferencia (B-A)", "Diferencia Simétrica", "Complemento"]

        ttk.Label(top_operacion, text="Conjunto 1:", style='TLabel').pack(pady=5)
        combo_conjunto1 = tk.StringVar(top_operacion)
        combo_conjunto1.set(letras_conjuntos[0] if letras_conjuntos else "")
        opciones_conjunto1 = ttk.OptionMenu(top_operacion, combo_conjunto1, *letras_conjuntos)
        opciones_conjunto1.pack(pady=5, padx=10, fill='x')
        self.combo_conjunto1 = combo_conjunto1 # Guardar referencia si es necesario

        ttk.Label(top_operacion, text="Operación:", style='TLabel').pack(pady=5)
        combo_operacion = tk.StringVar(top_operacion)
        combo_operacion.set(operaciones[0])
        opciones_operacion = ttk.OptionMenu(top_operacion, combo_operacion, *operaciones, command=self._actualizar_interfaz_operacion)
        opciones_operacion.pack(pady=5, padx=10, fill='x')
        self.combo_operacion = combo_operacion # Guardar referencia

        self.frame_conjunto2 = ttk.Frame(top_operacion, style='TFrame') # Frame para el Conjunto 2
        self.frame_conjunto2.pack(pady=5, fill='x')
        ttk.Label(self.frame_conjunto2, text="Conjunto 2:", style='TLabel').pack(side='left', padx=5)
        combo_conjunto2 = tk.StringVar(self.frame_conjunto2)
        combo_conjunto2.set(letras_conjuntos[1] if len(letras_conjuntos) > 1 else (letras_conjuntos[0] if letras_conjuntos else ""))
        opciones_conjunto2 = ttk.OptionMenu(self.frame_conjunto2, combo_conjunto2, *letras_conjuntos)
        opciones_conjunto2.pack(side='left', padx=5, fill='x', expand=True)
        self.combo_conjunto2 = combo_conjunto2 # Guardar referencia

        btn_graficar_operacion = ttk.Button(top_operacion, text="Graficar Operación", command=self._graficar_operacion)
        btn_graficar_operacion.pack(pady=10, padx=20, fill='x')

        self._actualizar_interfaz_operacion(operaciones[0]) # Inicializar la interfaz

    def _actualizar_interfaz_operacion(self, operacion):
        if operacion == "Complemento":
            self.frame_conjunto2.pack_forget() # Ocultar la selección del segundo conjunto
        else:
            self.frame_conjunto2.pack(pady=5, fill='x') # Mostrar la selección del segundo conjunto

    def _graficar_operacion(self):
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.patches as patches
        import numpy as np

        conjunto1_letra = self.combo_conjunto1.get()
        operacion_seleccionada = self.combo_operacion.get()
        conjunto2_letra = self.combo_conjunto2.get()

        conjuntoA = set(self.conjuntos.get(conjunto1_letra, []))
        conjuntoB = set(self.conjuntos.get(conjunto2_letra, []))
        resultado = set()

        if operacion_seleccionada == "Unión":
            resultado = conjuntoA.union(conjuntoB)
        elif operacion_seleccionada == "Intersección":
            resultado = conjuntoA.intersection(conjuntoB)
        elif operacion_seleccionada == "Diferencia (A-B)":
            resultado = conjuntoA.difference(conjuntoB)
        elif operacion_seleccionada == "Diferencia (B-A)":
            resultado = conjuntoB.difference(conjuntoA)
        elif operacion_seleccionada == "Diferencia Simétrica":
            resultado = conjuntoA.symmetric_difference(conjuntoB)
        elif operacion_seleccionada == "Complemento":
            if not self.universo:
                messagebox.showerror("Error", "Por favor, ingrese el Conjunto Universo primero.")
                return
            resultado = set(self.universo) - conjuntoA
            conjuntoB_letra = "" # No se usa para el complemento

        # Crear una nueva ventana para mostrar el resultado
        ventana_resultado = tk.Toplevel(self.root, bg='#2E3440')
        ventana_resultado.title("Resultado de la Operación")
        ventana_resultado.attributes('-fullscreen', True)

        ttk.Label(ventana_resultado, text=f"Operación: {conjunto1_letra} {operacion_seleccionada} {conjunto2_letra if operacion_seleccionada != 'Complemento' else ''}", style='TLabel').pack(pady=10)
        ttk.Label(ventana_resultado, text=f"Resultado: {', '.join(map(str, sorted(list(resultado))))}", style='TLabel').pack(pady=5)

        # Crear un gráfico
        fig_operacion, ax_operacion = plt.subplots(figsize=(8, 6))
        ax_operacion.set_aspect('equal')
        ax_operacion.axis('off')
        ax_operacion.set_xlim(-2, 2)
        ax_operacion.set_ylim(-2, 2)

        # Dibujar el universo para el complemento
        if operacion_seleccionada == "Complemento":
            rect_universo = patches.Rectangle((-2, -2), 4, 4, linewidth=1, edgecolor='black', facecolor='#EEEEEE', label='Universo')
            ax_operacion.add_patch(rect_universo)
            complemento_elementos = sorted(list(resultado))
            # Ajustar el tamaño de la fuente y el bbox
            ax_operacion.text(0, -1.5, f"Universo - {conjunto1_letra}: {', '.join(complemento_elementos)}", ha='center', fontsize=8, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

        # Dibujar los dos círculos
        circle1 = plt.Circle((-0.5, 0), 1, color='red', alpha=0.4, label=conjunto1_letra)
        circle2 = plt.Circle((0.5, 0), 1, color='blue', alpha=0.4, label=conjunto2_letra)
        ax_operacion.add_artist(circle1)
        ax_operacion.add_artist(circle2)
        ax_operacion.legend(loc='upper right')

        # Calcular las regiones para mostrar elementos
        solo_A = sorted(list(conjuntoA - conjuntoB))
        solo_B = sorted(list(conjuntoB - conjuntoA))
        interseccion = sorted(list(conjuntoA.intersection(conjuntoB)))

        # Función para ajustar el texto dentro de un área
        def ajustar_texto(ax, texto, x, y, max_width=0.3, max_lines=2, fontsize=8, **kwargs):
            words = texto.split(', ')
            lines = []
            current_line = []
            for word in words:
                test_line = current_line + [word]
                text_obj = ax.text(x, y, ', '.join(test_line), fontsize=fontsize, ha='center', va='center', **kwargs)
                bbox = text_obj.get_window_extent(renderer=ax.figure.canvas.get_renderer())
                bbox_width_norm = bbox.width / fig_operacion.dpi / (ax.get_xlim()[1] - ax.get_xlim()[0])
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
                text_obj = ax.text(x, y + y_offset, line, fontsize=fontsize, ha='center', va='center', **kwargs)
                y_offset -= 0.15 # Ajustar el espaciado entre líneas
            if len(lines) > max_lines:
                ax.text(x, y + y_offset - 0.15, "...", fontsize=fontsize, ha='center', va='center', **kwargs)


        # Posicionar el texto de los elementos con ajuste
        ajustar_texto(ax_operacion, ", ".join(solo_A), -0.8, 0.1, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
        ajustar_texto(ax_operacion, ", ".join(solo_B), 0.8, 0.1, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
        ajustar_texto(ax_operacion, ", ".join(interseccion), 0, -0.3, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

        # Sombreado de las áreas según la operación
        resolution = 500
        x_grid, y_grid = np.meshgrid(np.linspace(-2, 2, resolution), np.linspace(-2, 2, resolution))

        mask_circle1 = (x_grid + 0.5)**2 + y_grid**2 <= 1
        mask_circle2 = (x_grid - 0.5)**2 + y_grid**2 <= 1
        mask_universo = (x_grid >= -2) & (x_grid <= 2) & (y_grid >= -2) & (y_grid <= 2)

        alpha_sombreado = 0.4

        if operacion_seleccionada == "Unión":
            mask_resultado = mask_circle1 | mask_circle2
            ax_operacion.contourf(x_grid, y_grid, mask_resultado, levels=[0.5, 1], colors='none', hatches=['///'], alpha=alpha_sombreado)
        elif operacion_seleccionada == "Intersección":
            mask_resultado = mask_circle1 & mask_circle2
            ax_operacion.contourf(x_grid, y_grid, mask_resultado, levels=[0.5, 1], colors='none', hatches=['\\\\\\'], alpha=alpha_sombreado)
        elif operacion_seleccionada == "Diferencia (A-B)":
            mask_resultado = mask_circle1 & ~mask_circle2
            ax_operacion.contourf(x_grid, y_grid, mask_resultado, levels=[0.5, 1], colors='none', hatches=['...'], alpha=alpha_sombreado)
        elif operacion_seleccionada == "Diferencia (B-A)":
            mask_resultado = ~mask_circle1 & mask_circle2
            ax_operacion.contourf(x_grid, y_grid, mask_resultado, levels=[0.5, 1], colors='none', hatches=['xx'], alpha=alpha_sombreado)
        elif operacion_seleccionada == "Diferencia Simétrica":
            mask_resultado = (mask_circle1 & ~mask_circle2) | (~mask_circle1 & mask_circle2)
            ax_operacion.contourf(x_grid, y_grid, mask_resultado, levels=[0.5, 1], colors='none', hatches=['oo'], alpha=alpha_sombreado)
        elif operacion_seleccionada == "Complemento":
            mask_resultado = mask_universo & ~mask_circle1
            ax_operacion.contourf(x_grid, y_grid, mask_resultado, levels=[0.5, 1], colors='none', hatches=['|||'], alpha=alpha_sombreado)

        canvas_operacion = FigureCanvasTkAgg(fig_operacion, master=ventana_resultado)
        canvas_operacion_widget = canvas_operacion.get_tk_widget()
        canvas_operacion_widget.pack(expand=True, fill='both')
        canvas_operacion.draw()

        ttk.Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy, style='TButton').pack(pady=10)    

    def open_edit_window(self):
        if not self.conjuntos:
            tk.messagebox.showerror("Error", "No hay conjuntos para editar. Por favor, ingrese conjuntos primero.")
            return

        self.top_editar = tk.Toplevel(self.root, bg='#2E3440')
        self.top_editar.title("Editar Conjuntos y Universo")

        # --- Sección para editar el Universo ---
        frame_universo = ttk.Frame(self.top_editar)
        frame_universo.pack(pady=10, padx=10, fill='x')
        ttk.Label(frame_universo, text="Conjunto Universo = {", style='TLabel').pack(side='left')
        universo_str = ", ".join(sorted(list(self.universo)))
        self.universo_var_editar = tk.StringVar(value=universo_str)
        entry_universo_editar = ttk.Entry(frame_universo, textvariable=self.universo_var_editar, width=50)
        entry_universo_editar.pack(side='left', expand=True)
        ttk.Label(frame_universo, text="}", style='TLabel').pack(side='left')
        entry_universo_editar.bind("<FocusOut>", self._ordenar_elementos_universo_editar)
        entry_universo_editar.bind("<Return>", self._ordenar_elementos_universo_editar)

        self.entry_editar_vars = {}
        self.entry_editar = {}

        available_letters = sorted(list(self.conjuntos.keys()))

        for letra in available_letters:
            frame_conjunto = ttk.Frame(self.top_editar)
            frame_conjunto.pack(pady=5, padx=10, fill='x')

            ttk.Label(frame_conjunto, text=f"Conjunto {letra} = {{", width=10, anchor='w', style='TLabel').pack(side='left')

            elementos_str = ", ".join(sorted(list(self.conjuntos[letra])))
            var = tk.StringVar(value=elementos_str)
            entry = ttk.Entry(frame_conjunto, textvariable=var, width=40)
            entry.pack(side='left', expand=True)
            entry.bind("<FocusOut>", lambda event, l=letra: self._validar_elementos_en_universo_editar(event, l))
            entry.bind("<FocusOut>", self._ordenar_elementos_editar)
            entry.bind("<Return>", self._ordenar_elementos_editar)
            entry.bind("<Return>", lambda event, l=letra: self._validar_elementos_en_universo_editar(event, l))
            entry.bind("<FocusOut>", lambda event, l=letra: self._validar_cantidad_elementos_editar(event, l))
            entry.bind("<Return>", lambda event, l=letra: self._validar_cantidad_elementos_editar(event, l))

            ttk.Label(frame_conjunto, text="}", style='TLabel').pack(side='left')

            self.entry_editar_vars[letra] = var
            self.entry_editar[letra] = entry

        btn_guardar_ediciones = ttk.Button(self.top_editar, text="Guardar Ediciones", command=self._guardar_ediciones)
        btn_guardar_ediciones.pack(pady=10)

    def _ordenar_elementos_universo_editar(self, event):
        entry_widget = event.widget
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]

        def sort_key(item):
            try:
                num = float(item)
                if num == int(num):
                    return (0, int(num), item)
                else:
                    return (1, num, item)
            except ValueError:
                return (2, item)

        elementos_unicos_ordenados = sorted(list(set(elementos_lista)), key=sort_key)
        self.universo_var_editar.set(", ".join(elementos_unicos_ordenados))
    
    def _ordenar_elementos_universo_editar(self, event):
        entry_widget = event.widget
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]

        def sort_key(item):
            try:
                num = float(item)
                if num == int(num):
                    return (0, int(num), item)
                else:
                    return (1, num, item)
            except ValueError:
                return (2, item)

        elementos_unicos_ordenados = sorted(list(set(elementos_lista)), key=sort_key)
        self.universo_var_editar.set(", ".join(elementos_unicos_ordenados))

    def _ordenar_elementos_editar(self, event):
        entry_widget = event.widget
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
        elementos_unicos = sorted(list(set(elementos_lista)))
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ", ".join(elementos_unicos))

    def _validar_elementos_en_universo_editar(self, event, letra):
        entry_widget = self.entry_editar[letra]
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
        elementos_invalidos = set(elementos_lista) - self.universo
        if elementos_invalidos:
            messagebox.showerror("Error", f"El Conjunto {letra} contiene elementos no presentes en el Universo: {', '.join(sorted(list(elementos_invalidos)))}")
            # No limpiar el campo aquí para permitir la corrección en la edición

    def _validar_cantidad_elementos_editar(self, event, letra):
        entry_widget = self.entry_editar[letra]
        elementos_str = entry_widget.get()
        elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
        if len(set(elementos_lista)) > 15:
            messagebox.showerror("Error", f"El Conjunto {letra} no puede tener más de 15 elementos.")
            # No limpiar el campo en la edición para permitir la corrección

    def _guardar_ediciones(self):
        nuevos_conjuntos = {}
        errores = {}
        universo_str = self.universo_var_editar.get()
        self.universo = set([elem.strip() for elem in universo_str.split(',') if elem.strip()])

        for letra, var in self.entry_editar_vars.items():
            elementos_str = var.get()
            elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
            elementos_unicos = set(elementos_lista)

            # Validar cantidad máxima de elementos
            if len(elementos_unicos) > 15:
                errores[letra] = f"El Conjunto {letra} excede el máximo de 15 elementos ({len(elementos_unicos)})."

            # Validar elementos dentro del universo
            elementos_invalidos = elementos_unicos - self.universo
            if elementos_invalidos:
                if letra not in errores:
                    errores[letra] = ""
                errores[letra] += f" Contiene elementos no presentes en el Universo: {', '.join(sorted(list(elementos_invalidos)))}."
                errores[letra] = errores[letra].lstrip()

            if len(elementos_lista) != len(elementos_unicos) and elementos_lista:
                duplicados = [elem for elem in elementos_lista if elementos_lista.count(elem) > 1]
                if letra not in errores:
                    errores[letra] = ""
                errores[letra] += f" Se encontraron duplicados: {', '.join(sorted(list(set(duplicados))))}."
                errores[letra] = errores[letra].lstrip()

            nuevos_conjuntos[letra] = sorted(list(elementos_unicos))

        if errores:
            mensaje_error = "Se encontraron los siguientes errores:\n"
            for letra, error in errores.items():
                mensaje_error += f"{letra}: {error}\n"
            tk.messagebox.showerror("Errores en la Edición", mensaje_error)
        else:
            self.conjuntos = nuevos_conjuntos
            self.top_editar.destroy() # Usar el atributo de la clase