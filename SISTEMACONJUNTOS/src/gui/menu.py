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

        self._crear_campos_conjuntos(cantidad)

    def _crear_campos_conjuntos(self, cantidad_inicial=2):
        self.top_input = tk.Toplevel(self.root, bg='#2E3440')
        self.top_input.title("Ingresar Datos de Conjuntos")
        self.top_input.grab_set()

        self.frame_conjuntos = {}
        self.conjuntos_data = {}
        self.cantidad_var = tk.IntVar(value=0) # Para controlar la cantidad actual de conjuntos
        self.cantidad_var.set(0)
        self.frame_principal_conjuntos = ttk.Frame(self.top_input)
        self.frame_principal_conjuntos.pack(pady=5, padx=10, fill='both', expand=True)
        self.canvas_conjuntos = tk.Canvas(self.frame_principal_conjuntos, bg='#2E3440', highlightthickness=0)
        self.scrollbar_conjuntos = ttk.Scrollbar(self.frame_principal_conjuntos, orient=tk.VERTICAL, command=self.canvas_conjuntos.yview)
        self.scrollable_frame_conjuntos = ttk.Frame(self.canvas_conjuntos, style='TFrame')

        self.canvas_conjuntos.configure(yscrollcommand=self.scrollbar_conjuntos.set)
        self.scrollable_frame_conjuntos.bind("<Configure>", lambda e: self.canvas_conjuntos.configure(scrollregion=self.canvas_conjuntos.bbox("all")))
        self.canvas_conjuntos.create_window((0, 0), window=self.scrollable_frame_conjuntos, anchor="nw", width=780) # Ajustar ancho según necesidad

        self.scrollbar_conjuntos.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_conjuntos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.botones_eliminar = {} # Para almacenar referencias a los botones de eliminar

        for i in range(cantidad_inicial):
            self._agregar_campo_conjunto()

        frame_botones = ttk.Frame(self.top_input, style='TFrame')
        frame_botones.pack(pady=10)

        self.btn_agregar = ttk.Button(frame_botones, text="Agregar Conjunto", command=self._agregar_campo_conjunto)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self.btn_guardar = ttk.Button(frame_botones, text="Guardar Conjuntos", command=self.guardar_conjuntos, state=tk.DISABLED)
        self.btn_guardar.pack(side=tk.RIGHT, padx=5)

        self._actualizar_boton_guardar()
        self.root.wait_window(self.top_input)

    def _crear_campos_conjuntos(self, cantidad_inicial=2):
        self.top_input = tk.Toplevel(self.root, bg='#2E3440')
        self.top_input.title("Ingresar Datos de Conjuntos")
        self.top_input.grab_set()

        self.top_input.geometry("800x600")

        self.frame_conjuntos = {}
        self.conjuntos_data = {}
        self.cantidad_var = tk.IntVar(value=0)
        self.cantidad_var.set(0)
        self.frame_principal_conjuntos = ttk.Frame(self.top_input)
        self.frame_principal_conjuntos.pack(pady=5, padx=10, fill='both', expand=True)
        self.canvas_conjuntos = tk.Canvas(self.frame_principal_conjuntos, bg='#2E3440', highlightthickness=0)
        self.scrollbar_conjuntos = ttk.Scrollbar(self.frame_principal_conjuntos, orient=tk.VERTICAL, command=self.canvas_conjuntos.yview)
        self.scrollable_frame_conjuntos = ttk.Frame(self.canvas_conjuntos, style='TFrame')

        self.canvas_conjuntos.configure(yscrollcommand=self.scrollbar_conjuntos.set)
        self.scrollable_frame_conjuntos.bind("<Configure>", lambda e: self.canvas_conjuntos.configure(scrollregion=self.canvas_conjuntos.bbox("all")))
        self.canvas_conjuntos.create_window((0, 0), window=self.scrollable_frame_conjuntos, anchor="nw", width=780)

        self.scrollbar_conjuntos.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_conjuntos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.botones_eliminar = {}

        frame_botones = ttk.Frame(self.top_input, style='TFrame')
        frame_botones.pack(pady=10)

        self.btn_agregar = ttk.Button(frame_botones, text="Agregar Conjunto", command=self._agregar_campo_conjunto)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self.btn_guardar = ttk.Button(frame_botones, text="Guardar Conjuntos", command=self.guardar_conjuntos, state=tk.DISABLED)
        self.btn_guardar.pack(side=tk.RIGHT, padx=5)

        for i in range(cantidad_inicial):
            self._agregar_campo_conjunto()

        self._actualizar_boton_guardar()
        self.root.wait_window(self.top_input)

    def _agregar_campo_conjunto(self):
        cantidad_actual = self.cantidad_var.get()
        if cantidad_actual < 10:
            frame_conjunto = ttk.Frame(self.scrollable_frame_conjuntos)
            frame_conjunto.pack(pady=5, padx=10, fill='x')

            letra_var = tk.StringVar()
            available = self._obtener_letras_disponibles()
            default_letter = available[0] if available else (self.available_letters[cantidad_actual] if cantidad_actual < len(self.available_letters) else "")
            letra_var.set(default_letter)

            combo_letras = ttk.Combobox(frame_conjunto, textvariable=letra_var, values=sorted(self.available_letters), width=3)
            combo_letras.pack(side='left')
            combo_letras.bind("<<ComboboxSelected>>", self._validar_letras_duplicadas)
            combo_letras.bind("<FocusOut>", self._validar_letras_duplicadas)

            ttk.Label(frame_conjunto, text=" = {", width=4, anchor='w', style='TLabel').pack(side='left')

            entry = ttk.Entry(frame_conjunto, width=40)
            entry.pack(side='left', expand=True)
            entry.bind("<FocusOut>", self._ordenar_elementos)
            entry.bind("<Return>", self._ordenar_elementos)
            entry.bind("<FocusOut>", self._validar_cantidad_elementos)
            entry.bind("<Return>", self._validar_cantidad_elementos)

            ttk.Label(frame_conjunto, text="}", style='TLabel').pack(side='left')

            btn_eliminar = ttk.Button(frame_conjunto, text="Eliminar", command=lambda f=frame_conjunto: self._eliminar_campo_conjunto(f))
            btn_eliminar.pack(side=tk.LEFT, padx=5)
            self.botones_eliminar[frame_conjunto] = btn_eliminar

            self.frame_conjuntos[frame_conjunto] = (letra_var, entry, combo_letras)
            self.conjuntos_data[letra_var.get()] = set()
            self.cantidad_var.set(self.cantidad_var.get() + 1)
            self._actualizar_boton_guardar()

    def _eliminar_campo_conjunto(self, frame_a_eliminar):
        if self.cantidad_var.get() > 2:
            if frame_a_eliminar in self.frame_conjuntos:
                letra_var, _, combo = self.frame_conjuntos.pop(frame_a_eliminar)
                letra = letra_var.get()
                if letra in self.conjuntos_data:
                    del self.conjuntos_data[letra]
                if frame_a_eliminar in self.botones_eliminar:
                    self.botones_eliminar.pop(frame_a_eliminar).destroy()
                frame_a_eliminar.destroy()
                self.cantidad_var.set(self.cantidad_var.get() - 1)
                self._actualizar_letras_disponibles()
                self._validar_letras_duplicadas() # Revalidar duplicados al eliminar
                self._actualizar_boton_guardar()

    def _actualizar_letras_disponibles(self):
        used_letters = set([v[0].get() for _, v in self.frame_conjuntos.items()])
        for frame, (letra_var, _, combo) in self.frame_conjuntos.items():
            current_letter = letra_var.get()
            new_values = sorted([letter for letter in self.available_letters if letter not in used_letters or letter == current_letter])
            combo['values'] = new_values
            if current_letter not in new_values:
                letra_var.set(new_values[0] if new_values else "")

    def _validar_letras_duplicadas(self, event=None):
        letras = [v[0].get().strip() for _, v in self.frame_conjuntos.items()]
        letras_validas = [l for l in letras if l]
        duplicados = len(letras_validas) != len(set(letras_validas))
        self._actualizar_boton_guardar(duplicados)

    def _actualizar_boton_guardar(self, hay_duplicados=False):
        num_conjuntos = self.cantidad_var.get()
        letras = [v[0].get().strip() for _, v in self.frame_conjuntos.items()]
        letras_validas = [l for l in letras if l]
        suficientes_conjuntos = num_conjuntos >= 2

        if suficientes_conjuntos and not hay_duplicados and all(letras_validas):
            self.btn_guardar.config(state=tk.NORMAL)
        else:
            self.btn_guardar.config(state=tk.DISABLED)

    def _obtener_letras_disponibles(self):
        used_letters = set([v[0].get() for _, v in self.frame_conjuntos.items()])
        return sorted([letter for letter in self.available_letters if letter not in used_letters])

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
        elementos_universo = set()
        for frame, (letra_var, entry, _) in self.frame_conjuntos.items():
            letra = letra_var.get()
            elementos_str = entry.get()
            elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
            elementos_unicos = set(elementos_lista)
            elementos_universo.update(elementos_unicos) # <--- AQUÍ SE CONSTRUYE EL UNIVERSO

            if len(elementos_unicos) > 15:
                errores[letra] = f"El Conjunto {letra} excede el máximo de 15 elementos ({len(elementos_unicos)})."

            if len(elementos_lista) != len(elementos_unicos) and elementos_lista:
                duplicados = [elem for elem in elementos_lista if elementos_lista.count(elem) > 1]
                if letra not in errores:
                    errores[letra] = ""
                errores[letra] += f" Se encontraron duplicados: {', '.join(sorted(list(set(duplicados))))}."
                errores[letra] = errores[letra].lstrip()

            self.conjuntos[letra] = sorted(list(elementos_unicos))

        self.universo = sorted(list(elementos_universo)) # <--- SE GUARDA EL UNIVERSO CONSTRUIDO

        if errores:
            mensaje_error = "Se encontraron los siguientes errores:\n"
            for letra, error in errores.items():
                mensaje_error += f"{letra}: {error}\n"
            tk.messagebox.showerror("Errores al Guardar", mensaje_error)
        else:
            print("Guardando conjuntos:", self.conjuntos)
            print("Universo automático:", self.universo)
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
            descripcion_texto += f"Conjunto {letra} = {{ {', '.join(map(str, conjunto))} }}\n"

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
        if not self.conjuntos or len(self.conjuntos) < 1:
            messagebox.showerror("Error", "Debe haber al menos un conjunto ingresado para realizar una operación.")
            return

        self.top_operacion = tk.Toplevel(self.root, bg='#2E3440')
        self.top_operacion.title("Realizar Operación")
        self.top_operacion.grab_set()

        letras_conjuntos = sorted(self.conjuntos.keys())

        ttk.Label(self.top_operacion, text="Seleccione el primer conjunto:", style='TLabel').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.combo_conjunto1 = ttk.Combobox(self.top_operacion, values=letras_conjuntos, state='readonly')
        self.combo_conjunto1.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        if letras_conjuntos:
            self.combo_conjunto1.current(0) # Establecer el primer conjunto por defecto

        ttk.Label(self.top_operacion, text="Seleccione la operación:", style='TLabel').grid(row=1, column=0, padx=10, pady=10, sticky='w')
        operaciones = ["Unión", "Intersección", "Diferencia (A-B)", "Diferencia (B-A)", "Diferencia Simétrica", "Complemento"]
        self.combo_operacion = ttk.Combobox(self.top_operacion, values=operaciones, state='readonly')
        self.combo_operacion.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.combo_operacion.current(0) # Establecer "Unión" por defecto
        self.combo_operacion.bind("<<ComboboxSelected>>", self.actualizar_segundo_combo)

        self.label_conjunto2 = ttk.Label(self.top_operacion, text="Seleccione el segundo conjunto:", style='TLabel')
        self.label_conjunto2.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.combo_conjunto2 = ttk.Combobox(self.top_operacion, values=letras_conjuntos, state='readonly')
        self.combo_conjunto2.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        if len(letras_conjuntos) > 1:
            self.combo_conjunto2.current(1)
        elif letras_conjuntos:
            self.combo_conjunto2.current(0)

        # Llamar a la función inicialmente para establecer el estado correcto al abrir la ventana
        self.actualizar_segundo_combo()

        btn_realizar = ttk.Button(self.top_operacion, text="Realizar Operación y Graficar", command=self._graficar_operacion)
        btn_realizar.grid(row=3, column=0, columnspan=2, padx=10, pady=20, sticky='ew')

        self.root.wait_window(self.top_operacion)

    def actualizar_segundo_combo(self, event=None):
        operacion = self.combo_operacion.get()
        letras_conjuntos = sorted(self.conjuntos.keys())
        if operacion == "Complemento":
            self.label_conjunto2.config(state=tk.DISABLED)
            self.combo_conjunto2.config(state=tk.DISABLED)
        else:
            self.label_conjunto2.config(state=tk.NORMAL)
            self.combo_conjunto2.config(state='readonly')
            self.combo_conjunto2['values'] = letras_conjuntos
            if len(letras_conjuntos) > 1 and self.combo_conjunto1.get() == self.combo_conjunto2.get():
                # Asegurarse de que el segundo combo no tenga la misma selección que el primero inicialmente
                index_primer_conjunto = letras_conjuntos.index(self.combo_conjunto1.get())
                nuevo_index_segundo = (index_primer_conjunto + 1) % len(letras_conjuntos)
                self.combo_conjunto2.current(nuevo_index_segundo)
            elif letras_conjuntos and not self.combo_conjunto2.get():
                self.combo_conjunto2.current(0)

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
            if not self.conjuntos:
                messagebox.showerror("Error", "Por favor, ingrese conjuntos primero para realizar el complemento.")
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

        if operacion_seleccionada == "Complemento":
            # Dibujar el universo
            rect_universo = patches.Rectangle((-2, -2), 4, 4, linewidth=1, edgecolor='black', facecolor='#EEEEEE', label='Universo')
            ax_operacion.add_patch(rect_universo)
            # Definir la máscara para el círculo del conjunto A
            resolution = 500
            x_grid, y_grid = np.meshgrid(np.linspace(-2, 2, resolution), np.linspace(-2, 2, resolution))
            mask_circulo_a = (x_grid)**2 + (y_grid)**2 <= 1
            # Sombrear el área del complemento (Universo - Conjunto A)
            mask_complemento = (x_grid >= -2) & (x_grid <= 2) & (y_grid >= -2) & (y_grid <= 2) & ~mask_circulo_a
            ax_operacion.contourf(x_grid, y_grid, mask_complemento, levels=[0.5, 1], colors='none', hatches=['|||'], alpha=0.4)
            # Centrar el círculo para el conjunto A
            circulo_complemento = plt.Circle((0, 0), 1, color='lightblue', alpha=0.6, edgecolor='black')
            ax_operacion.add_artist(circulo_complemento)
            elementos_a_texto = ", ".join(sorted(list(conjuntoA)))
            fontsize_a = 12 if len(conjuntoA) < 8 else 8
            ax_operacion.text(0, 0, f"{conjunto1_letra} = {{{elementos_a_texto}}}", ha='center', va='center', fontsize=fontsize_a, color='black', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
            # Mostrar el complemento fuera del círculo
            complemento_elementos = sorted(list(set(self.universo) - conjuntoA))
            if complemento_elementos:
                complemento_texto = ", ".join(complemento_elementos)
                fontsize_complemento = 10 if len(complemento_elementos) < 12 else 7
                ax_operacion.text(0, -1.5, f"Complemento de {conjunto1_letra}: {{{complemento_texto}}}", ha='center', fontsize=fontsize_complemento, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
        else:
            # Dibujar los dos círculos para las otras operaciones
            circle1 = plt.Circle((-0.5, 0), 1, color='red', alpha=0.4, label=conjunto1_letra)
            circle2 = plt.Circle((0.5, 0), 1, color='blue', alpha=0.4, label=conjunto2_letra)
            ax_operacion.add_artist(circle1)
            ax_operacion.add_artist(circle2)
            ax_operacion.legend(loc='upper right')

            # Calcular las regiones para mostrar elementos
            solo_A = sorted(list(conjuntoA - conjuntoB))
            solo_B = sorted(list(conjuntoB - conjuntoA))
            interseccion = sorted(list(conjuntoA.intersection(conjuntoB)))

            def ajustar_texto(ax, texto, x, y, max_width=0.3, max_lines=2, fontsize=8, **kwargs):
                words = texto.split(', ')
                lines = []
                current_line = []
                for word in words:
                    test_line = current_line + [word]
                    text_obj = ax.text(x, y, ', '.join(test_line), fontsize=fontsize, ha='center', va='center', **kwargs)
                    bbox = text_obj.get_window_extent(renderer=ax.figure.canvas.get_renderer())
                    bbox_width_norm = bbox.width / fig_operacion.dpi / (ax.get_xlim()[1] - ax.get_xlim()[0])
                    text_obj.remove()
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
                    y_offset -= 0.15
                if len(lines) > max_lines:
                    ax.text(x, y + y_offset - 0.15, "...", fontsize=fontsize, ha='center', va='center', **kwargs)

            ajustar_texto(ax_operacion, ", ".join(solo_A), -0.8, 0.1, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
            ajustar_texto(ax_operacion, ", ".join(solo_B), 0.8, 0.1, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
            ajustar_texto(ax_operacion, ", ".join(interseccion), 0, -0.3, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

            resolution = 500
            x_grid, y_grid = np.meshgrid(np.linspace(-2, 2, resolution), np.linspace(-2, 2, resolution))
            mask_circle1 = (x_grid + 0.5)**2 + y_grid**2 <= 1
            mask_circle2 = (x_grid - 0.5)**2 + y_grid**2 <= 1

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
        self.top_editar.title("Editar Conjuntos")
        self.top_editar.geometry("800x600")

        self.frame_principal_editar = ttk.Frame(self.top_editar)
        self.frame_principal_editar.pack(pady=5, padx=10, fill='both', expand=True)
        self.canvas_editar = tk.Canvas(self.frame_principal_editar, bg='#2E3440', highlightthickness=0)
        self.scrollbar_editar = ttk.Scrollbar(self.frame_principal_editar, orient=tk.VERTICAL, command=self.canvas_editar.yview)
        self.scrollable_frame_editar = ttk.Frame(self.canvas_editar, style='TFrame')

        self.canvas_editar.configure(yscrollcommand=self.scrollbar_editar.set)
        self.scrollable_frame_editar.bind("<Configure>", lambda e: self.canvas_editar.configure(scrollregion=self.canvas_editar.bbox("all")))
        self.canvas_editar.create_window((0, 0), window=self.scrollable_frame_editar, anchor="nw", width=780)

        self.scrollbar_editar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_editar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame_universo_editar = ttk.Frame(self.scrollable_frame_editar)
        frame_universo_editar.pack(pady=10, padx=10, fill='x')
        ttk.Label(frame_universo_editar, text="Conjunto Universo = {", style='TLabel').pack(side='left')
        universo_str = ", ".join(sorted(list(self.universo)))
        self.universo_var_editar = tk.StringVar(value=universo_str)
        entry_universo_editar = ttk.Entry(frame_universo_editar, textvariable=self.universo_var_editar, width=50, state=tk.DISABLED)
        entry_universo_editar.pack(side='left', expand=True)
        ttk.Label(frame_universo_editar, text="}", style='TLabel').pack(side='left')

        self.entry_editar_vars = {}
        self.entry_editar = {}
        self.botones_eliminar_editar = {}
        self.btn_guardar_ediciones = None

        available_letters = sorted(list(self.conjuntos.keys()))
        self.cantidad_conjuntos_editar = tk.IntVar(value=len(self.conjuntos))

        for letra in available_letters:
            self._agregar_campo_editar(letra=letra, elementos=self.conjuntos[letra])

        frame_botones_editar = ttk.Frame(self.top_editar, style='TFrame')
        frame_botones_editar.pack(pady=10)

        self.btn_agregar_editar = ttk.Button(frame_botones_editar, text="Agregar Conjunto", command=self._agregar_campo_editar)
        self.btn_agregar_editar.pack(side=tk.LEFT, padx=5)

        self.btn_guardar_ediciones = ttk.Button(frame_botones_editar, text="Guardar Ediciones", command=self._guardar_ediciones)
        self.btn_guardar_ediciones.pack(side=tk.RIGHT, padx=5)

        self._validar_boton_guardar_editar() # Llamar SOLO al final de open_edit_window

    def _agregar_campo_editar(self, letra=None, elementos=None):
        cantidad_actual = self.cantidad_conjuntos_editar.get()
        if cantidad_actual < 10:
            frame_conjunto = ttk.Frame(self.scrollable_frame_editar)
            frame_conjunto.pack(pady=5, padx=10, fill='x')

            letra_var = tk.StringVar(value=letra if letra else self._obtener_letra_disponible_editar())

            combo_letras = ttk.Combobox(frame_conjunto, textvariable=letra_var, values=sorted(self.available_letters), width=3)
            combo_letras.pack(side='left')
            combo_letras.bind("<<ComboboxSelected>>", self._validar_letras_duplicadas_editar)
            combo_letras.bind("<FocusOut>", self._validar_letras_duplicadas_editar)
            combo_letras.bind("<KeyRelease>", self._validar_letras_duplicadas_editar)

            ttk.Label(frame_conjunto, text=" = {", width=4, anchor='w', style='TLabel').pack(side='left')

            elementos_str = ", ".join(sorted(elementos)) if elementos else ""
            var = tk.StringVar(value=elementos_str)
            entry = ttk.Entry(frame_conjunto, textvariable=var, width=40)
            entry.pack(side='left', expand=True)
            entry.bind("<FocusOut>", self._ordenar_elementos_editar)
            entry.bind("<Return>", self._ordenar_elementos_editar)
            entry.bind("<FocusOut>", lambda event, l=letra_var.get(): self._validar_cantidad_elementos_editar(event, l))
            entry.bind("<Return>", lambda event, l=letra_var.get(): self._validar_cantidad_elementos_editar(event, l))

            ttk.Label(frame_conjunto, text="}", style='TLabel').pack(side='left')

            btn_eliminar_editar = ttk.Button(frame_conjunto, text="Eliminar", command=lambda f=frame_conjunto: self._eliminar_campo_editar(f, letra_var.get()))
            btn_eliminar_editar.pack(side=tk.LEFT, padx=5)
            self.botones_eliminar_editar[frame_conjunto] = btn_eliminar_editar

            self.entry_editar_vars[frame_conjunto] = (letra_var, var, combo_letras)
            self.entry_editar[letra_var.get()] = entry
            self.cantidad_conjuntos_editar.set(self.cantidad_conjuntos_editar.get() + 1)
            self._actualizar_letras_disponibles_editar()
            # self._validar_boton_guardar_editar() <--- ELIMINADO DE AQUÍ

    def _eliminar_campo_editar(self, frame_a_eliminar, letra_eliminada):
        cantidad_actual = self.cantidad_conjuntos_editar.get()
        if cantidad_actual > 2:
            if frame_a_eliminar in self.entry_editar_vars:
                del self.entry_editar_vars[frame_a_eliminar]
            if letra_eliminada in self.entry_editar:
                del self.entry_editar[letra_eliminada]
            if frame_a_eliminar in self.botones_eliminar_editar:
                self.botones_eliminar_editar.pop(frame_a_eliminar).destroy()
            frame_a_eliminar.destroy()
            self.cantidad_conjuntos_editar.set(self.cantidad_conjuntos_editar.get() - 1)
            self._actualizar_letras_disponibles_editar(letra_eliminada)
            self._validar_letras_duplicadas_editar()

    def _obtener_letra_disponible_editar(self):
        used_letters = set(self.entry_editar_vars.keys())
        for letter in self.available_letters:
            if letter not in used_letters:
                return letter
        return "" # No hay letras disponibles

    def _actualizar_letras_disponibles_editar(self, letra_eliminada=None):
        used_letters = set([data[0].get() for frame, data in self.entry_editar_vars.items()])
        for frame, (letra_var, var, combo) in self.entry_editar_vars.items():
            current_letter = letra_var.get()
            new_values = sorted([letter for letter in self.available_letters if letter not in used_letters or letter == current_letter or letter == letra_eliminada])
            combo['values'] = new_values
            if current_letter not in new_values:
                letra_var.set(new_values[0] if new_values else "")

    def _validar_letras_duplicadas_editar(self, event=None):
        letras = [data[0].get().strip() for data in self.entry_editar_vars.values()]
        letras_validas = [l for l in letras if l]
        hay_duplicados = len(letras_validas) != len(set(letras_validas))
        self._validar_boton_guardar_editar(hay_duplicados)
        return hay_duplicados

    def _validar_boton_guardar_editar(self, hay_duplicados=False):
        num_conjuntos = self.cantidad_conjuntos_editar.get()
        letras = [data[0].get().strip() for data in self.entry_editar_vars.values()]
        letras_validas = [l for l in letras if l]
        cantidad_valida = 2 <= num_conjuntos <= 10

        if cantidad_valida and not hay_duplicados and all(letras_validas):
            # Buscar si todas las letras son diferentes de las originales (si se está editando)
            letras_originales = set(self.conjuntos.keys())
            letras_actuales = set(letras_validas)
            if letras_originales == letras_actuales:
                self.btn_guardar_ediciones.config(state=tk.NORMAL) # Habilitar si no hay cambios en las letras
            elif letras_actuales.issuperset(letras_originales) and len(letras_actuales) == len(letras_originales):
                 self.btn_guardar_ediciones.config(state=tk.NORMAL) # Habilitar si solo se modificaron elementos
            else:
                self.btn_guardar_ediciones.config(state=tk.NORMAL) # Habilitar si las letras son válidas y diferentes
        else:
            self.btn_guardar_ediciones.config(state=tk.DISABLED)

    def _validar_cantidad_conjuntos_editar(self):
        cantidad = self.cantidad_conjuntos_editar.get()
        if not 2 <= cantidad <= 10:
            tk.messagebox.showerror("Error", f"La cantidad de conjuntos debe estar entre 2 y 10 (actualmente: {cantidad}).")
            return False
        return True

    def _ordenar_elementos_editar(self, event):
        entry = event.widget
        elements_str = entry.get()
        elements_list = [elem.strip() for elem in elements_str.split(',') if elem.strip()]
        elements_unicos_ordenados = sorted(list(set(elements_list)))
        entry.delete(0, tk.END)
        entry.insert(0, ", ".join(elements_unicos_ordenados))

    def _validar_cantidad_elementos_editar(self, event, letra):
        entry_var = self.entry_editar_vars[letra]
        elementos = [elem.strip() for elem in entry_var.get().split(',') if elem.strip()]
        if len(set(elementos)) > 15:
            tk.messagebox.showerror("Error", f"El Conjunto {letra} excede el máximo de 15 elementos.")

    # ... (Asegúrate de que tu método _guardar_ediciones esté actualizado para no usar el universo de la edición)

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

        for frame, data in self.entry_editar_vars.items():
            letra_var, entry_var, _ = data
            letra = letra_var.get().strip()
            elementos_str = entry_var.get()
            elementos_lista = [elem.strip() for elem in elementos_str.split(',') if elem.strip()]
            elementos_unicos = set(elementos_lista)

            if len(elementos_unicos) > 15:
                if letra not in errores:
                    errores[letra] = ""
                errores[letra] += f" El Conjunto {letra} excede el máximo de 15 elementos ({len(elementos_unicos)})."

            if len(elementos_lista) != len(elementos_unicos) and elementos_lista:
                duplicados = [elem for elem in elementos_lista if elementos_lista.count(elem) > 1]
                if letra not in errores:
                    errores[letra] = ""
                errores[letra] += f" Se encontraron duplicados en el Conjunto {letra}: {', '.join(sorted(list(set(duplicados))))}."
                errores[letra] = errores[letra].lstrip()

            nuevos_conjuntos[letra] = sorted(list(elementos_unicos))

        if not self._validar_cantidad_conjuntos_editar():
            return

        if self._validar_letras_duplicadas_editar():
            return

        if errores:
            mensaje_error = "Se encontraron los siguientes errores:\n"
            for letra, error in errores.items():
                mensaje_error += f"{letra}: {error}\n"
            tk.messagebox.showerror("Errores en la Edición", mensaje_error)
        else:
            self.conjuntos = nuevos_conjuntos
            # --- Lógica para actualizar el universo ---
            todos_los_elementos = set()
            for conjunto in self.conjuntos.values():
                todos_los_elementos.update(conjunto)
            self.universo = sorted(list(todos_los_elementos))
            print(f"Universo automático después de editar: {self.universo}")
            # --- Fin de la lógica de actualización del universo ---
            if self.top_editar:
                self.top_editar.destroy()
