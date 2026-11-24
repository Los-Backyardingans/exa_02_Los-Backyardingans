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

#Devuelve la localidad del reporte, aunque falte la ubicación
def localidad_de(reporte: dict) -> str:
    return (reporte.get("ubicacion") or {}).get("localidad") or "Sin localidad"
