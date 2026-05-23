import csv
import os

RUTA_ESTUDIANTES = "data/estudiantes.csv"
RUTA_ASISTENCIA  = "data/asistencia.csv"


CABECERA_ESTUDIANTES = ["id","apellidos","nombres","dni","grado","seccion","turno"]
CABECERA_ASISTENCIA  = ["estudiante_id","fecha","estado","observacion"]


def leer_csv(ruta, cabecera):
    
   
    if not os.path.exists(ruta):
        escribir_csv(ruta, cabecera, []) 
        return []

    registros = []

    #abrir el archivo en modo lectura
    with open(ruta, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)  

        #recorrer cada fila del CSV
        for fila in lector:
            registros.append(fila)

    return registros


def escribir_csv(ruta, cabecera, registros):
    
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:

        escritor = csv.DictWriter(archivo, fieldnames=cabecera)
        escritor.writeheader()      

        #escribir cada registro como una fila
        for registro in registros:
            escritor.writerow(registro)
    
def obtener_estudiantes():

    return leer_csv(RUTA_ESTUDIANTES, CABECERA_ESTUDIANTES)


def buscar_estudiante_por_id(id):
   
    estudiantes = obtener_estudiantes()

    #recorrer todos hasta encontrar el que coincide
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


def generar_nuevo_id():
    estudiantes = obtener_estudiantes()

    if len(estudiantes) == 0:
        return 1

    id_maximo = 0
    for e in estudiantes:
        id_actual = int(e["id"])

        if id_actual > id_maximo:
            id_maximo = id_actual

    return id_maximo + 1



def agregar_estudiante(apellidos, nombres, dni, grado, seccion, turno):


    if buscar_estudiante_por_dni(dni) is not None:
        return False

    estudiantes = obtener_estudiantes()

    nuevo = {
        "id":       generar_nuevo_id(),
        "apellidos": apellidos.strip(),
        "nombres":   nombres.strip(),
        "dni":       dni.strip(),
        "grado":     grado,
        "seccion":   seccion,
        "turno":     turno
    }

    estudiantes.append(nuevo)

    escribir_csv(RUTA_ESTUDIANTES, CABECERA_ESTUDIANTES, estudiantes)
    return True



def actualizar_estudiante(id, apellidos, nombres, dni, grado, seccion, turno):
    estudiantes = obtener_estudiantes()

    for e in estudiantes:
        if e["id"] == str(id):
            e["apellidos"] = apellidos.strip()
            e["nombres"]   = nombres.strip()
            e["dni"]       = dni.strip()
            e["grado"]     = grado
            e["seccion"]   = seccion
            e["turno"]     = turno
            break   

    escribir_csv(RUTA_ESTUDIANTES, CABECERA_ESTUDIANTES, estudiantes)


def eliminar_estudiante(id):

    estudiantes = obtener_estudiantes()

    #crear una nueva lista excluyendo al eliminado
    nueva_lista = []
    for e in estudiantes:
        if e["id"] != str(id):
            nueva_lista.append(e)

    escribir_csv(RUTA_ESTUDIANTES, CABECERA_ESTUDIANTES, nueva_lista)

    eliminar_asistencia_por_estudiante(id)


def filtrar_estudiantes(buscar="", grado=""):

    estudiantes = obtener_estudiantes()
    resultado   = []

    for e in estudiantes:


        nombre_completo = e["apellidos"] + " " + e["nombres"]

        coincide_texto = buscar.lower() in nombre_completo.lower() \
                      or buscar in e["dni"]


        if buscar == "" and grado == "":
            resultado.append(e)
        elif buscar != "" and grado == "" and coincide_texto:
            resultado.append(e)
        elif buscar == "" and grado != "" and e["grado"] == grado:
            resultado.append(e)
        elif buscar != "" and grado != "" and coincide_texto and e["grado"] == grado:
            resultado.append(e)

    return resultado


def obtener_asistencia():
    
    return leer_csv(RUTA_ASISTENCIA, CABECERA_ASISTENCIA)


def obtener_asistencia_por_grupo(grado, seccion, fecha):
    
    asistencia   = obtener_asistencia()
    estudiantes  = filtrar_estudiantes(grado=grado)
    registros    = {}

    for e in estudiantes:
        if e["seccion"] != seccion:
            continue   

        for reg in asistencia:
            if reg["estudiante_id"] == e["id"] and reg["fecha"] == fecha:
                registros[e["id"]] = reg
                break  

    return registros


def guardar_asistencia(estudiante_id, fecha, estado, observacion):
    
    asistencia = obtener_asistencia()
    encontrado = False

    #buscar si ya existe un registro para ese día
    i = 0
    while i < len(asistencia):
        reg = asistencia[i]

        if reg["estudiante_id"] == str(estudiante_id) and reg["fecha"] == fecha:
            asistencia[i]["estado"]      = estado
            asistencia[i]["observacion"] = observacion
            encontrado = True
            break

        i += 1


    if not encontrado:
        asistencia.append({
            "estudiante_id": str(estudiante_id),
            "fecha":         fecha,
            "estado":        estado,
            "observacion":   observacion
        })

    escribir_csv(RUTA_ASISTENCIA, CABECERA_ASISTENCIA, asistencia)


def eliminar_asistencia_por_estudiante(estudiante_id):
    
    asistencia  = obtener_asistencia()
    nueva_lista = []

    for reg in asistencia:
        if reg["estudiante_id"] != str(estudiante_id):
            nueva_lista.append(reg)

    escribir_csv(RUTA_ASISTENCIA, CABECERA_ASISTENCIA, nueva_lista)


def calcular_resumen(fecha=""):
    
    asistencia   = obtener_asistencia()
    presentes    = 0
    tardanzas    = 0
    faltas       = 0
    justificados = 0

    for reg in asistencia:

        #filtrar por fecha
        if fecha != "" and reg["fecha"] != fecha:
            continue


        if reg["estado"] == "P":
            presentes += 1
        elif reg["estado"] == "T":
            tardanzas += 1
        elif reg["estado"] == "F":
            faltas += 1
        elif reg["estado"] == "J":
            justificados += 1

    return {
        "presentes":     presentes,
        "tardanzas":     tardanzas,
        "faltas":        faltas,
        "justificados":  justificados
    }


def resumen_por_grado():
    """
    Calcula el resumen de asistencia agrupado por grado.
    Devuelve una lista de diccionarios, uno por grado.
    """
    grados     = ["1ro", "2do", "3ro", "4to", "5to"]
    asistencia = obtener_asistencia()
    resultado  = []


    for grado in grados:
        estudiantes_grado = filtrar_estudiantes(grado=grado)
        ids_grado = []

        for e in estudiantes_grado:
            ids_grado.append(e["id"])

        presentes  = 0
        tardanzas  = 0
        faltas     = 0


        for reg in asistencia:
            if reg["estudiante_id"] in ids_grado:
                if reg["estado"] == "P":
                    presentes += 1
                elif reg["estado"] == "T":
                    tardanzas += 1
                elif reg["estado"] == "F":
                    faltas += 1

        resultado.append({
            "grado":     grado,
            "alumnos":   len(estudiantes_grado),
            "presentes": presentes,
            "tardanzas": tardanzas,
            "faltas":    faltas
        })

    return resultado