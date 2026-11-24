
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

