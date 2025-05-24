import tkinter as tk
from tkinter import ttk, messagebox
import random

class SimulacionTalleres:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación Montecarlo - Talleres CapacitaYa")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f2f5')
        
        # Variables por defecto
        self.capacidad_max = 30
        self.ganancia_por_persona = 100
        self.costo_por_rechazado = 150  # Valor fijo, no modificable
        
        # Distribuciones de probabilidad por defecto
        self.distribuciones = {
            31: {28: 0.10, 29: 0.25, 30: 0.50, 31: 0.15},
            32: {28: 0.05, 29: 0.25, 30: 0.50, 31: 0.15, 32: 0.05},
            33: {29: 0.05, 30: 0.20, 31: 0.45, 32: 0.20, 33: 0.10},
            34: {29: 0.05, 30: 0.10, 31: 0.40, 32: 0.30, 33: 0.10, 34: 0.05}
        }
        
        # Configurar estilo básico
        self.configurar_estilos()
        
        # Crear widgets
        self.crear_widgets()
        
    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar solo estilos básicos que sabemos que funcionan
        self.style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), 
                       foreground='#2c3e50', background='#f0f2f5')
        
        self.style.configure('Modern.TButton', font=('Segoe UI', 11, 'bold'),
                       foreground='white', background='#3498db')
        self.style.map('Modern.TButton',
                 background=[('active', '#2980b9'), ('pressed', '#21618c')])
        
        self.style.configure('Success.TButton', font=('Segoe UI', 12, 'bold'),
                       foreground='white', background='#27ae60')
        self.style.map('Success.TButton',
                 background=[('active', '#229954'), ('pressed', '#1e8449')])
        
        self.style.configure('Modern.TEntry', fieldbackground='white',
                       borderwidth=1, relief='solid')
        
        self.style.configure('Modern.TCombobox', fieldbackground='white',
                       borderwidth=1, relief='solid')
        
        self.style.configure('Prob.TEntry', fieldbackground='#e8f4fd',
                       borderwidth=1, relief='solid', font=('Segoe UI', 10))
        
        self.style.configure('Disabled.TEntry', fieldbackground='#ecf0f1',
                       foreground='#95a5a6', borderwidth=1, relief='solid')
        
        # Estilo para la tabla
        self.style.configure('Modern.Treeview', background='white',
                       foreground='#2c3e50', font=('Segoe UI', 9))
        self.style.configure('Modern.Treeview.Heading', font=('Segoe UI', 10, 'bold'),
                       foreground='#2c3e50', background='#ecf0f1')
        
    def crear_widgets(self):
        # Canvas principal con scrollbar
        canvas = tk.Canvas(self.root, bg='#f0f2f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame principal dentro del scrollable
        main_frame = ttk.Frame(scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título principal
        title_frame = tk.Frame(main_frame, bg='#f0f2f5', height=80)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        title_frame.pack_propagate(False)
        
        titulo = ttk.Label(title_frame, text="🎯 Simulación Montecarlo", 
                          style='Title.TLabel')
        titulo.pack(pady=15)
        
        subtitulo = ttk.Label(title_frame, text="Optimización de Talleres CapacitaYa", 
                             font=('Segoe UI', 12), foreground='#7f8c8d',
                             background='#f0f2f5')
        subtitulo.pack()
        
        # Container principal con dos columnas
        container = ttk.Frame(main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda - Parámetros
        left_column = ttk.Frame(container)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Frame de parámetros
        params_frame = ttk.LabelFrame(left_column, text="⚙️ Parámetros de Simulación")
        params_frame.pack(fill=tk.X, pady=(0, 20), padx=5, ipady=10)
        
        # Grid para parámetros
        params_grid = ttk.Frame(params_frame)
        params_grid.pack(fill=tk.X, padx=15, pady=10)
        
        # Inscripciones
        ttk.Label(params_grid, text="📋 Inscripciones:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_inscripciones = ttk.Combobox(params_grid, values=[31, 32, 33, 34], 
                                               state="readonly", width=12, style='Modern.TCombobox')
        self.combo_inscripciones.set(32)
        self.combo_inscripciones.grid(row=0, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        self.combo_inscripciones.bind("<<ComboboxSelected>>", self.actualizar_probabilidades)
        
        # Experimentos
        ttk.Label(params_grid, text="🔬 Experimentos:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_experimentos = ttk.Entry(params_grid, width=12, style='Modern.TEntry')
        self.entry_experimentos.insert(0, "1000")
        self.entry_experimentos.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Ganancia por asistente
        ttk.Label(params_grid, text="💰 Ganancia por asistente:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_ganancia = ttk.Entry(params_grid, width=12, style='Modern.TEntry')
        self.entry_ganancia.insert(0, "100")
        self.entry_ganancia.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Separador visual (ahora en row=3 en lugar de row=4)
        sep = ttk.Separator(params_grid, orient='horizontal')
        sep.grid(row=3, column=0, columnspan=2, sticky='ew', pady=15)
        
        # Rango de visualización (ahora en row=4 en lugar de row=5)
        ttk.Label(params_grid, text="👁️ Visualización:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        range_frame = ttk.Frame(params_grid)    
        range_frame.grid(row=4, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        ttk.Label(range_frame, text="Desde:").pack(side=tk.LEFT)
        self.entry_desde = ttk.Entry(range_frame, width=8, style='Modern.TEntry')
        self.entry_desde.insert(0, "1")
        self.entry_desde.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(range_frame, text="Filas:").pack(side=tk.LEFT)
        self.entry_cantidad_filas = ttk.Entry(range_frame, width=8, style='Modern.TEntry')
        self.entry_cantidad_filas.insert(0, "10")
        self.entry_cantidad_filas.pack(side=tk.LEFT, padx=(5, 0))
        
        # Frame de probabilidades
        prob_frame = ttk.LabelFrame(left_column, text="📊 Distribución de Probabilidades")
        prob_frame.pack(fill=tk.X, pady=(0, 20), padx=5, ipady=10)
        
        # Headers
        header_frame = ttk.Frame(prob_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=(10, 15))
        
        ttk.Label(header_frame, text="👥 Asistentes", 
                 font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)
        ttk.Label(header_frame, text="📈 Probabilidad", 
                 font=('Segoe UI', 11, 'bold')).pack(side=tk.RIGHT)
        
        # Grid de probabilidades
        self.prob_entries = {}
        prob_grid = ttk.Frame(prob_frame)
        prob_grid.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        for i, asistentes in enumerate(range(28, 35)):
            row_frame = ttk.Frame(prob_grid)
            row_frame.pack(fill=tk.X, pady=2)
            
            # Label con ícono
            label_text = f"🔢 {asistentes} personas"
            ttk.Label(row_frame, text=label_text, width=18).pack(side=tk.LEFT)
            
            # Entry para probabilidad
            entry = ttk.Entry(row_frame, width=12, style='Prob.TEntry')
            entry.pack(side=tk.RIGHT)
            self.prob_entries[asistentes] = entry
        
        # Botón de simulación
        btn_frame = ttk.Frame(left_column)
        btn_frame.pack(fill=tk.X, pady=20, padx=5)
        
        btn_simular = ttk.Button(btn_frame, text="🚀 EJECUTAR SIMULACIÓN", 
                                style='Success.TButton',
                                command=self.ejecutar_simulacion)
        btn_simular.pack(fill=tk.X, ipady=10)
        
        # Columna derecha - Resultados
        right_column = ttk.Frame(container)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Frame de resultados
        resultados_frame = ttk.LabelFrame(right_column, text="📋 Resultados de la Simulación")
        resultados_frame.pack(fill=tk.BOTH, expand=True, padx=5, ipady=10)
        
        # Crear frame para la tabla con grid manager
        tabla_frame = ttk.Frame(resultados_frame)
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Configurar grid weights
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)
        
        # Crear Treeview
        columnas = ('Taller', 'RND', 'Asist', 'Fuera', 'Ingreso', 'Costo', 'Utilidad', 'Util.Tot', 'Util.Prom')
        self.tabla_resultados = ttk.Treeview(tabla_frame, columns=columnas, show='headings', 
                                           height=20, style='Modern.Treeview')
        
        # Configurar columnas
        headers = ['🎲 Taller', '🎯 RND', '👥 Asist', '🚫 Fuera', '💰 Ingreso', 
                  '💸 Costo', '💵 Utilidad', '📊 Util.Tot', '📈 Util.Prom']
        anchos = [80, 100, 70, 70, 100, 100, 100, 120, 120]
        
        for i, (col, header) in enumerate(zip(columnas, headers)):
            self.tabla_resultados.heading(col, text=header)
            self.tabla_resultados.column(col, width=anchos[i], anchor='center')
        
        # Scrollbars para la tabla - USANDO GRID CONSISTENTEMENTE
        scrollbar_v = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tabla_resultados.yview)
        scrollbar_h = ttk.Scrollbar(tabla_frame, orient=tk.HORIZONTAL, command=self.tabla_resultados.xview)
        self.tabla_resultados.config(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Posicionar usando grid
        self.tabla_resultados.grid(row=0, column=0, sticky='nsew')
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        # Frame para resumen
        resumen_frame = ttk.LabelFrame(right_column, text="📝 Resumen Ejecutivo")
        resumen_frame.pack(fill=tk.X, pady=(15, 0), padx=5, ipady=10)
        
        self.label_resumen = tk.Text(resumen_frame, height=8, wrap=tk.WORD, 
                                    font=('Segoe UI', 10), bg='#f8f9fa', 
                                    border=0, relief='flat')
        self.label_resumen.pack(fill=tk.X, padx=15, pady=10)
        self.label_resumen.insert('1.0', "🎯 Ejecute una simulación para ver los resultados detallados")
        self.label_resumen.config(state='disabled')
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind del mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Inicializar probabilidades
        self.actualizar_probabilidades()
        
    def actualizar_probabilidades(self, event=None):
        inscripciones = int(self.combo_inscripciones.get())
        distribucion = self.distribuciones[inscripciones]
        
        # Limpiar y deshabilitar todos los campos primero
        for asistentes in range(28, 35):
            entry = self.prob_entries[asistentes]
            entry.delete(0, tk.END)
            entry.config(state='disabled', style='Disabled.TEntry')
        
        # Habilitar y llenar solo los campos válidos
        for asistentes, prob in distribucion.items():
            if asistentes <= inscripciones:
                entry = self.prob_entries[asistentes]
                entry.config(state='normal', style='Prob.TEntry')
                entry.insert(0, str(prob))
            
    def validar_entradas(self):
        try:
            experimentos = int(self.entry_experimentos.get())
            if experimentos <= 0:
                messagebox.showerror("❌ Error", "La cantidad de experimentos debe ser mayor a 0")
                return False
                
            # Validar ganancia por asistente
            try:
                ganancia = float(self.entry_ganancia.get())
                if ganancia < 0:
                    messagebox.showerror("❌ Error", "La ganancia por asistente debe ser mayor o igual a 0")
                    return False
            except ValueError:
                messagebox.showerror("❌ Error", "Ganancia por asistente debe ser un número válido")
                return False
                
            # El costo por rechazado ahora es fijo, no necesita validación del input
            costo_rechazado = self.costo_por_rechazado
                
            desde = int(self.entry_desde.get())
            cantidad = int(self.entry_cantidad_filas.get())
            
            if desde <= 0:
                messagebox.showerror("❌ Error", "El número de fila inicial debe ser mayor a 0")
                return False
                
            if cantidad <= 0:
                messagebox.showerror("❌ Error", "La cantidad de filas a mostrar debe ser mayor a 0")
                return False
                
            if desde > experimentos:
                messagebox.showerror("❌ Error", "La fila inicial no puede ser mayor al total de experimentos")
                return False
                
            if desde + cantidad - 1 > experimentos:
                messagebox.showerror("❌ Error", f"El rango excede el total de experimentos ({experimentos})")
                return False
                
            inscripciones = int(self.combo_inscripciones.get())
            suma_prob = 0
            probabilidades = {}
            
            for asistentes in range(28, inscripciones + 1):
                entry = self.prob_entries[asistentes]
                if entry['state'] != 'disabled':
                    prob_str = entry.get().strip()
                    if prob_str:
                        try:
                            prob = float(prob_str)
                            if prob < 0 or prob > 1:
                                messagebox.showerror("❌ Error", f"La probabilidad para {asistentes} asistentes debe estar entre 0 y 1")
                                return False
                            probabilidades[asistentes] = prob
                            suma_prob += prob
                        except ValueError:
                            messagebox.showerror("❌ Error", f"Probabilidad inválida para {asistentes} asistentes")
                            return False
                            
            if abs(suma_prob - 1.0) > 0.001:
                messagebox.showerror("❌ Error", f"La suma de probabilidades debe ser 1.0 (actual: {suma_prob:.3f})")
                return False
                
            return True, experimentos, desde, cantidad, probabilidades, ganancia, costo_rechazado
            
        except ValueError:
            messagebox.showerror("❌ Error", "Por favor ingrese valores numéricos válidos")
            return False
            
    def generar_asistencia(self, probabilidades):
        rand = random.random()
        acum = 0
        
        for asistentes, prob in probabilidades.items():
            acum += prob
            if rand <= acum:
                return asistentes
        
        return max(probabilidades.keys())
        
    def calcular_utilidad(self, asistencia, inscripciones, ganancia_por_persona, costo_por_rechazado):
        if asistencia <= self.capacidad_max:
            ingreso = asistencia * ganancia_por_persona
            costo = 0
            cantidad_fuera = 0
        else:
            cantidad_fuera = asistencia - self.capacidad_max
            ingreso = self.capacidad_max * ganancia_por_persona
            costo = cantidad_fuera * costo_por_rechazado
            
        utilidad = ingreso - costo
        return utilidad, ingreso, costo, cantidad_fuera
        
    def ejecutar_simulacion(self):
        validacion = self.validar_entradas()
        if not validacion:
            return
            
        _, experimentos, desde, cantidad_filas, probabilidades, ganancia_por_persona, costo_por_rechazado = validacion
        inscripciones = int(self.combo_inscripciones.get())
        
        # Limpiar resultados previos
        for item in self.tabla_resultados.get_children():
            self.tabla_resultados.delete(item)
        
        fila_anterior = None
        fila_actual = None
        ultima_fila_datos = None
        filas_mostrar = []
        utilidad_total = 0
        
        if not probabilidades:
            messagebox.showerror("❌ Error", "No se encontraron probabilidades válidas")
            return
            
        for i in range(1, experimentos + 1):
            try:
                random_asistencia = random.random()
                asistencia = self.generar_asistencia(probabilidades)
                utilidad, ingreso, costo, cantidad_fuera = self.calcular_utilidad(asistencia, inscripciones, ganancia_por_persona, costo_por_rechazado)
                
                utilidad_total += utilidad
                utilidad_promedio = utilidad_total / i
                
                fila_anterior = fila_actual
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
                
                if desde <= i <= desde + cantidad_filas - 1:
                    filas_mostrar.append(fila_actual.copy())
                
                if i == experimentos:
                    ultima_fila_datos = fila_actual.copy()
                
            except Exception as e:
                messagebox.showerror("❌ Error", f"Error en la simulación (iteración {i}): {str(e)}")
                return
        
        # Insertar filas con colores alternos
        for idx, fila in enumerate(filas_mostrar):
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
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tabla_resultados.insert('', 'end', values=valores, tags=(tag,))
        
        # Agregar última fila si no está incluida
        if experimentos > desde + cantidad_filas - 1 and ultima_fila_datos:
            separador = ('━━━', '━━━ ÚLTIMA', 'FILA ━━━', '━━━', '━━━', '━━━', '━━━', '━━━', '━━━')
            self.tabla_resultados.insert('', 'end', values=separador, tags=('separador',))
            
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
        
        # Configurar colores de filas
        self.tabla_resultados.tag_configure('evenrow', background='#f8f9fa')
        self.tabla_resultados.tag_configure('oddrow', background='white')
        self.tabla_resultados.tag_configure('separador', background='#6c757d', foreground='white')
        self.tabla_resultados.tag_configure('ultima', background='#e3f2fd', foreground='#1565c0')
        
        # Mostrar resumen mejorado
        utilidad_final = utilidad_total / experimentos
        utilidad_sin_sobre = 28 * ganancia_por_persona
        diferencia = utilidad_final - utilidad_sin_sobre
        porcentaje = diferencia/utilidad_sin_sobre*100 if utilidad_sin_sobre != 0 else 0
        
        if diferencia > 0:
            icono = "✅"
            decision = "APLICAR SOBREINSCRIPCIÓN"
            color_decision = "#27ae60"
        else:
            icono = "❌"
            decision = "NO APLICAR SOBREINSCRIPCIÓN"
            color_decision = "#e74c3c"
        
        resumen_texto = f"""📊 RESULTADOS DE LA SIMULACIÓN
        
🎯 Inscripciones: {inscripciones} | 🔬 Experimentos: {experimentos:,}
💰 Utilidad Promedio: ${utilidad_final:,.2f}
📈 Diferencia vs Sin Sobreinscripción: ${diferencia:,.2f} ({porcentaje:+.1f}%)
💵 Ganancia por asistente: ${ganancia_por_persona:.0f} | 💸 Costo por rechazado: ${costo_por_rechazado:.0f}

{icono} RECOMENDACIÓN: {decision}"""
        
        self.label_resumen.config(state='normal')
        self.label_resumen.delete('1.0', tk.END)
        self.label_resumen.insert('1.0', resumen_texto)
        self.label_resumen.config(state='disabled')

def crear_interfaz():
    root = tk.Tk()
    app = SimulacionTalleres(root)
    root.mainloop()