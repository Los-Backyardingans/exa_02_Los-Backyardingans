#Consultas y agregaciones sobre la colección avistamientos en una provincia/cantón o categoría específica.

#importacion de las librerias
from datetime import datetime
from pymongo import MongoClient

# CONEXIÓN
MONGO_URI = "mongodb://admin:parda99%2A@127.0.0.1:27017/admin"
nombre_bd = "RCOFA"

# Rango de fechas que cubra los datos que genere el generador sintético.
fecha_inicio = datetime(2025, 1, 1, 0, 0, 0)
fecha_fin = datetime(2025, 12, 31, 23, 59, 59)


#FUNCIONES AUXILIARES
#=========================
meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Setiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

#devuelve el nombre del mes
def nombre_mes(numero_mes: int) -> str:
    return meses.get(numero_mes, "Mes desconocido")

#convierte el datetime a texto
def formatear_fecha(fecha) -> str:
    if fecha is None:
        return "Sin fecha"
    return f"{fecha.day} de {nombre_mes(fecha.month)} de {fecha.year}, {fecha:%H:%M}"

#deja solo los reportes cuya duración supere los "segundos"
def filtrar_mayores(reportes: list, segundos: int = 200) -> list:
    return [r for r in reportes if (r.get("duracion_seg") or 0) > segundos]


def filtrar_mayores_lambda(reportes: list, segundos: int = 200) -> list:
    return list(filter(lambda r: (r.get("duracion_seg") or 0) > segundos, reportes))


def obtener_db(cliente):
    return cliente[nombre_bd]

#Devuelve el código del reporte
def codigo_reporte(reporte: dict) -> str:
    return str(reporte.get("codigo_reporte", reporte.get("_id", "Sin código")))



# =======================================
# CONSULTA 1: filtro ($eq), proyección y ordenamiento múltiple
# =======================================
#Busca avistamientos por provincia, cantón y/o categoría usando $eq.
def consulta_filtro_proyeccion_orden(db, provincia=None, canton=None, id_categoria=None):
    avistamientos = db["avistamientos"]

    filtro = {}
    if provincia is not None:
        filtro["ubicacion.provincia"] = {"$eq": provincia}
    if canton is not None:
        filtro["ubicacion.canton"] = {"$eq": canton}
    if id_categoria is not None:
        filtro["id_categoria"] = {"$eq": id_categoria}

    proyeccion = {
        "codigo_reporte": 1,
        "fecha_evento": 1,
        "duracion_seg": 1,
        "ubicacion.localidad": 1,
        # El _id se devuelve por defecto; sirve de respaldo si no hay codigo_reporte
    }

    cursor = avistamientos.find(filtro, proyeccion).sort([
        ("duracion_seg", -1),   # duración descendente
        ("fecha_evento", 1),    # fecha ascendente
    ])
    return list(cursor)

#imprime la consulta 1
def imprimir_consulta_1(resultados, limite=15):
    print("Total encontrados:", len(resultados))
    for r in resultados[:limite]:
        localidad = r.get("ubicacion", {}).get("localidad", "Sin localidad")
        print(codigo_reporte(r), "|", formatear_fecha(r.get("fecha_evento")), "|",
              r.get("duracion_seg", "N/D"), "seg |", localidad)


# =======================================
# CONSULTA 2: rango de fechas ($gte y $lte)
# =======================================
def consulta_rango_fechas(db, inicio, fin):
    avistamientos = db["avistamientos"]
    filtro = {"fecha_evento": {"$gte": inicio, "$lte": fin}}
    return list(avistamientos.find(filtro))

#imprime la consulta 2
def imprimir_consulta_2(resultados, limite=15):
    print("Total en el rango:", len(resultados))
    for r in resultados[:limite]:
        print(codigo_reporte(r), "|", formatear_fecha(r.get("fecha_evento")))


# =======================================
# CONSULTA 3: agregación con dos $lookup
# =======================================
def agregacion_lookup(db):
    avistamientos = db["avistamientos"]

    pipeline = [
        {"$lookup": {
            "from": "categorias_fenomeno",
            "localField": "id_categoria",
            "foreignField": "_id",
            "as": "categoria",
        }},
        {"$lookup": {
            "from": "observadores",
            "localField": "id_observador",
            "foreignField": "_id",
            "as": "observador",
        }},
        # $lookup devuelve una lista; $unwind la convierte en un solo documento
        {"$unwind": "$categoria"},
        {"$unwind": "$observador"},
    ]
    return list(avistamientos.aggregate(pipeline))

#metodo que imprime la agregación
def imprimir_agregacion(resultados, limite=15):
    print("Total de reportes:", len(resultados))
    for r in resultados[:limite]:
        localidad = r.get("ubicacion", {}).get("localidad", "Sin localidad")
        print(codigo_reporte(r), "|", r["categoria"]["nombre"], "|",
              r["observador"]["alias_o_estacion"], "|", localidad)
