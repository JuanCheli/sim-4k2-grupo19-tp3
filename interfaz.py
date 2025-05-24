import tkinter as tk
from tkinter import ttk, messagebox
import random
from tabla import crear_fila_tabla

class SimulacionTalleres:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación Montecarlo - Talleres CapacitaYa")
        self.root.geometry("1200x800")
        
        # Variables por defecto
        self.capacidad_max = 30
        self.ganancia_por_persona = 100
        self.costo_por_rechazado = 150
        
        # Distribuciones de probabilidad por defecto
        self.distribuciones = {
            31: {28: 0.10, 29: 0.25, 30: 0.50, 31: 0.15},
            32: {28: 0.05, 29: 0.25, 30: 0.50, 31: 0.15, 32: 0.05},
            33: {29: 0.05, 30: 0.20, 31: 0.45, 32: 0.20, 33: 0.10},
            34: {29: 0.05, 30: 0.10, 31: 0.40, 32: 0.30, 33: 0.10, 34: 0.05}
        }
        
        self.crear_widgets()
        
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo = ttk.Label(main_frame, text="Simulación de Talleres - CapacitaYa", 
                          font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Frame de parámetros
        params_frame = ttk.LabelFrame(main_frame, text="Parámetros de Simulación", padding=15)
        params_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Cantidad de inscripciones
        ttk.Label(params_frame, text="Cantidad de Inscripciones:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.combo_inscripciones = ttk.Combobox(params_frame, values=[31, 32, 33, 34], 
                                               state="readonly", width=10)
        self.combo_inscripciones.set(32)
        self.combo_inscripciones.grid(row=0, column=1, padx=(0, 20))
        self.combo_inscripciones.bind("<<ComboboxSelected>>", self.actualizar_probabilidades)
        
        # Cantidad de experimentos
        ttk.Label(params_frame, text="Cantidad de Experimentos:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.entry_experimentos = ttk.Entry(params_frame, width=10)
        self.entry_experimentos.insert(0, "1000")
        self.entry_experimentos.grid(row=0, column=3, padx=(0, 20))
        
        # Rango de filas a mostrar
        ttk.Label(params_frame, text="Desde fila:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.entry_desde = ttk.Entry(params_frame, width=10)
        self.entry_desde.insert(0, "1")
        self.entry_desde.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        
        ttk.Label(params_frame, text="Cantidad de filas:").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.entry_cantidad_filas = ttk.Entry(params_frame, width=10)
        self.entry_cantidad_filas.insert(0, "10")
        self.entry_cantidad_filas.grid(row=1, column=3, padx=(0, 20), pady=(10, 0))
        
        # Frame de probabilidades
        prob_frame = ttk.LabelFrame(main_frame, text="Distribución de Probabilidades", padding=15)
        prob_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Crear entries para probabilidades
        self.prob_entries = {}
        self.crear_campos_probabilidades(prob_frame)
        
        # Botón para simular
        btn_simular = ttk.Button(main_frame, text="Ejecutar Simulación", 
                                command=self.ejecutar_simulacion)
        btn_simular.pack(pady=10)
        
        # Frame de resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=15)
        resultados_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview para mostrar resultados en tabla
        columnas = ('Taller', 'RND', 'Asist', 'Fuera', 'Ingreso', 'Costo', 'Utilidad', 'Util.Tot', 'Util.Prom')
        self.tabla_resultados = ttk.Treeview(resultados_frame, columns=columnas, show='headings', height=15)
        
        # Configurar columnas
        anchos = [60, 80, 60, 60, 80, 80, 80, 100, 100]
        for i, col in enumerate(columnas):
            self.tabla_resultados.heading(col, text=col)
            self.tabla_resultados.column(col, width=anchos[i], anchor='center')
        
        # Scrollbars para la tabla
        scrollbar_v = ttk.Scrollbar(resultados_frame, orient=tk.VERTICAL, command=self.tabla_resultados.yview)
        scrollbar_h = ttk.Scrollbar(resultados_frame, orient=tk.HORIZONTAL, command=self.tabla_resultados.xview)
        self.tabla_resultados.config(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Empaquetar tabla y scrollbars
        self.tabla_resultados.grid(row=0, column=0, sticky='nsew')
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        resultados_frame.grid_rowconfigure(0, weight=1)
        resultados_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para resumen
        resumen_frame = ttk.LabelFrame(main_frame, text="Resumen", padding=10)
        resumen_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.label_resumen = ttk.Label(resumen_frame, text="Ejecute una simulación para ver los resultados", 
                                      font=("Arial", 10))
        self.label_resumen.pack()
        
        # Inicializar probabilidades
        self.actualizar_probabilidades()
        
    def crear_campos_probabilidades(self, parent):
        # Headers
        ttk.Label(parent, text="Asistentes", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        ttk.Label(parent, text="Probabilidad", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        
        # Crear entries para cada posible cantidad de asistentes (28-34)
        for i, asistentes in enumerate(range(28, 35)):
            ttk.Label(parent, text=str(asistentes)).grid(row=i+1, column=0, padx=5, pady=2)
            entry = ttk.Entry(parent, width=10)
            entry.grid(row=i+1, column=1, padx=5, pady=2)
            self.prob_entries[asistentes] = entry
            
    def actualizar_probabilidades(self, event=None):
        inscripciones = int(self.combo_inscripciones.get())
        distribucion = self.distribuciones[inscripciones]
        
        # Limpiar y deshabilitar todos los campos primero
        for asistentes in range(28, 35):
            entry = self.prob_entries[asistentes]
            entry.delete(0, tk.END)
            entry.config(state='disabled')
        
        # Habilitar y llenar solo los campos válidos (asistentes <= inscripciones)
        for asistentes, prob in distribucion.items():
            if asistentes <= inscripciones:
                entry = self.prob_entries[asistentes]
                entry.config(state='normal')
                entry.insert(0, str(prob))
            
    def validar_entradas(self):
        try:
            # Validar cantidad de experimentos
            experimentos = int(self.entry_experimentos.get())
            if experimentos <= 0:
                messagebox.showerror("Error", "La cantidad de experimentos debe ser mayor a 0")
                return False
                
            # Validar rango de filas
            desde = int(self.entry_desde.get())
            cantidad = int(self.entry_cantidad_filas.get())
            
            if desde <= 0:
                messagebox.showerror("Error", "El número de fila inicial debe ser mayor a 0")
                return False
                
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad de filas a mostrar debe ser mayor a 0")
                return False
                
            if desde > experimentos:
                messagebox.showerror("Error", "La fila inicial no puede ser mayor al total de experimentos")
                return False
                
            if desde + cantidad - 1 > experimentos:
                messagebox.showerror("Error", f"El rango excede el total de experimentos ({experimentos})")
                return False
                
            # Validar probabilidades
            inscripciones = int(self.combo_inscripciones.get())
            suma_prob = 0
            probabilidades = {}
            
            # Solo validar campos habilitados (asistentes <= inscripciones)
            for asistentes in range(28, inscripciones + 1):
                entry = self.prob_entries[asistentes]
                if entry['state'] != 'disabled':
                    prob_str = entry.get().strip()
                    if prob_str:
                        try:
                            prob = float(prob_str)
                            if prob < 0 or prob > 1:
                                messagebox.showerror("Error", f"La probabilidad para {asistentes} asistentes debe estar entre 0 y 1")
                                return False
                            probabilidades[asistentes] = prob
                            suma_prob += prob
                        except ValueError:
                            messagebox.showerror("Error", f"Probabilidad inválida para {asistentes} asistentes")
                            return False
                            
            if abs(suma_prob - 1.0) > 0.001:
                messagebox.showerror("Error", f"La suma de probabilidades debe ser 1.0 (actual: {suma_prob:.3f})")
                return False
                
            return True, experimentos, desde, cantidad, probabilidades
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
            return False
            
    def generar_asistencia(self, probabilidades):
        """Genera la cantidad de asistentes basado en las probabilidades"""
        rand = random.random()
        acum = 0
        
        for asistentes, prob in probabilidades.items():
            acum += prob
            if rand <= acum:
                return asistentes
        
        # Fallback al último valor si hay errores de redondeo
        return max(probabilidades.keys())
        
    def calcular_utilidad(self, asistencia, inscripciones):
        """Calcula la utilidad basada en la asistencia"""
        if asistencia <= self.capacidad_max:
            # Todos pueden entrar
            ingreso = asistencia * self.ganancia_por_persona
            costo = 0
            cantidad_fuera = 0
        else:
            # Algunos deben ser rechazados
            cantidad_fuera = asistencia - self.capacidad_max
            ingreso = self.capacidad_max * self.ganancia_por_persona
            costo = cantidad_fuera * self.costo_por_rechazado
            
        utilidad = ingreso - costo
        return utilidad, ingreso, costo, cantidad_fuera
        
    def ejecutar_simulacion(self):
        validacion = self.validar_entradas()
        if not validacion:
            return
            
        _, experimentos, desde, cantidad_filas, probabilidades = validacion
        inscripciones = int(self.combo_inscripciones.get())
        
        # Limpiar resultados previos
        for item in self.tabla_resultados.get_children():
            self.tabla_resultados.delete(item)
        
        # Variables para trabajar solo con 2 filas en memoria
        fila_anterior = None
        fila_actual = None
        ultima_fila_datos = None
        
        # Variables para almacenar solo las filas del rango solicitado
        filas_mostrar = []
        
        utilidad_total = 0
        
        # Debug: Verificar que tenemos probabilidades válidas
        if not probabilidades:
            messagebox.showerror("Error", "No se encontraron probabilidades válidas")
            return
            
        for i in range(1, experimentos + 1):
            try:
                random_asistencia = random.random()
                asistencia = self.generar_asistencia(probabilidades)
                utilidad, ingreso, costo, cantidad_fuera = self.calcular_utilidad(asistencia, inscripciones)
                
                utilidad_total += utilidad
                utilidad_promedio = utilidad_total / i
                
                # Mover fila actual a anterior
                fila_anterior = fila_actual
                
                # Crear datos de la fila actual
                fila_actual = {
                    'taller': i,
                    'random': random_asistencia,
                    'asistencia': asistencia,
                    'fuera': cantidad_fuera,
                    'ingreso': ingreso,
                    'costo': costo,
                    'utilidad': utilidad,
                    'utilidad_total': utilidad_total,
                    'utilidad_promedio': utilidad_promedio
                }
                
                # Guardar filas del rango solicitado
                if desde <= i <= desde + cantidad_filas - 1:
                    filas_mostrar.append(fila_actual.copy())
                
                # Siempre guardar la última fila
                if i == experimentos:
                    ultima_fila_datos = fila_actual.copy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error en la simulación (iteración {i}): {str(e)}")
                return
        
        # Insertar filas del rango solicitado en la tabla
        for fila in filas_mostrar:
            valores = (
                fila['taller'],
                f"{fila['random']:.4f}",
                fila['asistencia'],
                fila['fuera'],
                f"${fila['ingreso']:.0f}",
                f"${fila['costo']:.0f}",
                f"${fila['utilidad']:.0f}",
                f"${fila['utilidad_total']:.0f}",
                f"${fila['utilidad_promedio']:.2f}"
            )
            self.tabla_resultados.insert('', 'end', values=valores)
        
        # Agregar separador y última fila si no está incluida en el rango
        if experimentos > desde + cantidad_filas - 1 and ultima_fila_datos:
            # Insertar separador
            separador = ('---', '--- ÚLTIMA', 'FILA ---', '---', '---', '---', '---', '---', '---')
            self.tabla_resultados.insert('', 'end', values=separador, tags=('separador',))
            
            # Insertar última fila
            valores_ultima = (
                ultima_fila_datos['taller'],
                f"{ultima_fila_datos['random']:.4f}",
                ultima_fila_datos['asistencia'],
                ultima_fila_datos['fuera'],
                f"${ultima_fila_datos['ingreso']:.0f}",
                f"${ultima_fila_datos['costo']:.0f}",
                f"${ultima_fila_datos['utilidad']:.0f}",
                f"${ultima_fila_datos['utilidad_total']:.0f}",
                f"${ultima_fila_datos['utilidad_promedio']:.2f}"
            )
            self.tabla_resultados.insert('', 'end', values=valores_ultima, tags=('ultima',))
        
        # Configurar colores para las filas especiales
        self.tabla_resultados.tag_configure('separador', background='lightgray')
        self.tabla_resultados.tag_configure('ultima', background='lightblue')
        
        # Mostrar resumen
        utilidad_final = utilidad_total / experimentos
        utilidad_sin_sobre = 28 * self.ganancia_por_persona
        diferencia = utilidad_final - utilidad_sin_sobre
        
        if diferencia > 0:
            recomendacion = f"RECOMENDACIÓN: Aplicar sobreinscripción (+${diferencia:.2f}, +{diferencia/utilidad_sin_sobre*100:.1f}%)"
        else:
            recomendacion = f"RECOMENDACIÓN: NO aplicar sobreinscripción (${diferencia:.2f}, {diferencia/utilidad_sin_sobre*100:.1f}%)"
        
        resumen_texto = (f"Inscripciones: {inscripciones} | Experimentos: {experimentos} | "
                        f"Utilidad promedio: ${utilidad_final:.2f} | {recomendacion}")
        
        self.label_resumen.config(text=resumen_texto)

def crear_interfaz():
    root = tk.Tk()
    app = SimulacionTalleres(root)
    root.mainloop()