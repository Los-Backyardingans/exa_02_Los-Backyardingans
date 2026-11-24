from pymongo import MongoClient

# Conexion con MongoDB
MONGO_URI = "mongodb://admin:parda99%2A@127.0.0.1:27017/admin"

cliente = MongoClient(MONGO_URI)

# Comprobar la conexion
cliente.admin.command("ping")

print("Conexion con MongoDB exitosa")

# Seleccionar la base de datos
db = cliente["RCOFA"]

# Seleccionar la coleccion
observadores = db["observadores"]


# Metodo para insertar un observador
def insertar_observador():

    id_observador = int(input("Ingrese el ID del observador: "))
    alias = input("Ingrese el alias o estacion: ")
    rol = input("Ingrese el rol: ")
    confiabilidad = float(input("Ingrese el indice de confiabilidad (0 a 1): "))

    observador = {
        "_id": id_observador,
        "alias_o_estacion": alias,
        "rol": rol,
        "indice_confiabilidad": confiabilidad
    }

    resultado = observadores.insert_one(observador)

    print("Observador insertado correctamente")
    print("ID:", resultado.inserted_id)

    # Metodo para modificar un observador
    def modificar_observador():

        id_observador = int(input("Ingrese el ID del observador que desea modificar: "))

        alias = input("Ingrese el nuevo alias o estacion: ")
        rol = input("Ingrese el nuevo rol: ")
        confiabilidad = float(input("Ingrese el nuevo indice de confiabilidad (0 a 1): "))

        resultado = observadores.update_one(
            {"_id": id_observador},
            {
                "$set": {
                    "alias_o_estacion": alias,
                    "rol": rol,
                    "indice_confiabilidad": confiabilidad
                }
            }
        )

        if resultado.modified_count > 0:
            print("Observador modificado correctamente")
        else:
            print("No se encontro el observador o no hubo cambios")

