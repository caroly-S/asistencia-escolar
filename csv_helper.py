import csv
import os

# ── Rutas de los archivos CSV ──────────────────────────────
RUTA_ESTUDIANTES = "data/estudiantes.csv"
RUTA_ASISTENCIA  = "data/asistencia.csv"

# ── Cabeceras (columnas) de cada archivo ──────────────────
CABECERA_ESTUDIANTES = ["id","apellidos","nombres","dni","grado","seccion","turno"]
CABECERA_ASISTENCIA  = ["estudiante_id","fecha","estado","observacion"]


# ══════════════════════════════════════════════════════════
# MÉTODOS GENERALES: leer y escribir cualquier CSV
# ══════════════════════════════════════════════════════════

def leer_csv(ruta, cabecera):
    """
    Lee un archivo CSV y devuelve una lista de diccionarios.
    Si el archivo no existe, lo crea vacío con sus cabeceras.
    """
    # if verifica si el archivo existe
    if not os.path.exists(ruta):
        escribir_csv(ruta, cabecera, [])   # lo crea vacío
        return []

    registros = []

    # Abre el archivo en modo lectura
    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)   # lee cada fila como diccionario

        # for recorre cada fila del CSV
        for fila in lector:
            registros.append(fila)

    return registros


def escribir_csv(ruta, cabecera, registros):
    """
    Escribe una lista de diccionarios en un archivo CSV.
    Sobreescribe todo el archivo (así funciona el UPDATE y DELETE).
    """
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=cabecera)
        escritor.writeheader()       # escribe la primera fila (cabeceras)

        # for escribe cada registro como una fila
        for registro in registros:
            escritor.writerow(registro)
    
def obtener_estudiantes():

    return leer_csv(RUTA_ESTUDIANTES, CABECERA_ESTUDIANTES)


def buscar_estudiante_por_id(id):
   
    estudiantes = obtener_estudiantes()

    
    for e in estudiantes:
        if e["id"] == str(id):     
            return e

    return None


def buscar_estudiante_por_dni(dni):

    
    estudiantes = obtener_estudiantes()

    for e in estudiantes:
        
        if e["dni"] == dni.strip():
            return e

    return None

