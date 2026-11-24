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

