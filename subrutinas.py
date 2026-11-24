
"""
subrutinas.py
Funciones de apoyo reutilizables por todos los programas del examen
"""
from pymongo import MongoClient

# ---------------------------------------------------------------------------
# PASO: Listas dadas en el enunciado para clasificar el tipo de zona
# ---------------------------------------------------------------------------
CANTONES_COSTEROS = {
    "Puntarenas", "Esparza", "Montes de Oro", "Osa", "Quepos", "Golfito",
    "Parrita", "Corredores", "Garabito", "Liberia", "Nicoya", "Santa Cruz",
    "Bagaces", "Carrillo", "Cañas", "Abangares", "Nandayure", "La Cruz",
    "Hojancha", "Limón", "Pococí", "Siquirres", "Talamanca", "Matina",
    "Guácimo",
}
CANTONES_MONTANOSOS = {
    "Tarrazú", "Aserrí", "Mora", "Acosta", "Turrubares", "Dota",
    "Pérez Zeledón", "León Cortés", "Puriscal", "San Ramón", "Zarcero",
    "Poás", "Valverde Vega", "Paraíso", "Jiménez", "Turrialba", "Alvarado",
    "Oreamuno", "El Guarco", "Barva", "Santa Bárbara", "San Rafael",
    "San Isidro", "Tilarán", "Buenos Aires", "Coto Brus",
}
POBLADOS_INSULARES = {
    "Isla del Coco", "Isla Chira", "Isla Venado", "Isla Caballo",
    "Isla San Lucas", "Isla Tortuga", "Isla Cedros", "Isla Jesucita",
    "Isla Berrugate",
}

def clasificar_tipo_zona(provincia: str, canton: str, poblado: str) -> str:
    """
    Determina el tipo_zona de una localidad.
    Orden de prioridad (lo más específico primero):
      1. Poblado insular  -> "Insular"
      2. Cantón costero   -> "Costera"
      3. Cantón montañoso -> "Montañosa"
      4. Cualquier otro   -> "Urbana"
    """

    #Recibe los datos de una localidad y devuelve uno de los cuatro valores posibles de tipo_zona:
    if poblado.strip() in POBLADOS_INSULARES:
        return "Insular"
    if canton.strip() in CANTONES_COSTEROS:
        return "Costera"
    if canton.strip() in CANTONES_MONTANOSOS:
        return "Montañosa"
    return "Urbana"

# ---------------------------------------------------------------------------
# PASO: Utilidades de formato
# ---------------------------------------------------------------------------
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]


def formatear_fecha(fecha) -> str:
    #Devuelve la fecha como '15 de Octubre de 2025, 14:30' (mes 10 = Octubre)."""
    return f"{fecha.day} de {MESES[fecha.month - 1]} de {fecha.year}, {fecha:%H:%M}"


def generar_codigo_reporte(numero: int) -> str:
    #Genera el código 'REP-' + 8 dígitos con ceros a la izquierda."""
    return f"REP-{numero:08d}"

# ---------------------------------------------------------------------------
# PASO: Generador de avistamientos sintéticos
# ---------------------------------------------------------------------------
def generar_avistamientos(bd, cantidad=10_000):
    """
    Genera 'cantidad' avistamientos sintéticos NO uniformes en la colección
    avistamientos. Usa las ubicaciones, categorías y observadores ya cargados.
    """
    bd.avistamientos.drop()  # evita duplicados al ejecutar varias veces

    # Datos de referencia que ya están en la base de datos
    ubicaciones = list(bd.ubicaciones.find())
    ids_categoria = [c["_id"] for c in bd.categorias_fenomeno.find({}, {"_id": 1})]
    ids_observador = [o["_id"] for o in bd.observadores.find({}, {"_id": 1})]

    # Rango de fechas aleatorias: del 1/ene/2024 al 1/feb/2026
    inicio = datetime(2024, 1, 1)
    rango_seg = int((datetime(2026, 2, 1) - inicio).total_seconds())
