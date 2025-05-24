# Función para crear la tabla
def crear_fila_tabla(taller, random_asistencia, asistencia, cantidad_fuera, ingreso_asistencia, costo_echar, utilidad, utilidad_total, utilidad_promedio):
    fila = {
        "Taller": taller,
        "Random Asistencia": random_asistencia,
        "Asistencia": asistencia,
        "Cantidad Fuera": cantidad_fuera,
        "Ingreso Asistencia": ingreso_asistencia,
        "Costo Echar": costo_echar,
        "Utilidad": utilidad,
        "Utilidad Total": utilidad_total,
        "Utilidad Promedio": utilidad_promedio
    }
    return fila