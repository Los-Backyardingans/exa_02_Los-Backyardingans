# Descripción: Genera 10 000 avistamientos
# sintéticos en MongoDB.

from pymongo import MongoClient
from subrutinas import generar_avistamientos

# Conexión con MongoDB
MONGO_URI = "mongodb://admin:parda99%2A@127.0.0.1:27017/admin"

cliente = MongoClient(MONGO_URI)

try:
    # Comprobar conexión
    cliente.admin.command("ping")
    print("Conexión con MongoDB exitosa")

    # Seleccionar base de datos
    db = cliente["RCOFA"]

    # Ejecutar generador
    generar_avistamientos(db, 10000)

    # Comprobar cantidad de registros
    total = db.avistamientos.count_documents({})

    print("Total de avistamientos:", total)

except Exception as error:
    print("Error:", error)

finally:
    cliente.close()
    print("Conexión cerrada")
