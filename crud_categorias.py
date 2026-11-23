
from pymongo import MongoClient

# Conexion con MongoDB
MONGO_URI =  "mongodb://127.0.0.1:27017/"

cliente = MongoClient(MONGO_URI)

# Comprobar la conexion
cliente.admin.command("ping")

print("Conexion con MongoDB exitosa")

# Seleccionar la base de datos
db = cliente["RCOFA"]

# Seleccionar la coleccion
categorias_fenomeno = db["categorias_fenomeno"]


# Metodo para insertar una categoria
def insertar_categoria():

    id_categoria = int(input("Ingrese el ID de la categoria: "))
    nombre = input("Ingrese el nombre de la categoria: ")
    descripcion = input("Ingrese la descripcion: ")

    categoria = {
        "_id": id_categoria,
        "nombre": nombre,
        "descripcion": descripcion
    }

    resultado = categorias_fenomeno.insert_one(categoria)

    print("Categoria insertada correctamente")
    print("ID:", resultado.inserted_id)



# Metodo para modificar una categoria
def modificar_categoria():

    id_categoria = int(input("Ingrese el ID de la categoria que desea modificar: "))

    nombre = input("Ingrese el nuevo nombre: ")
    descripcion = input("Ingrese la nueva descripcion: ")

    resultado = categorias_fenomeno.update_one(
        {"_id": id_categoria},
        {
            "$set": {
                "nombre": nombre,
                "descripcion": descripcion
            }
        }
    )

    if resultado.modified_count > 0:
        print("Categoria modificada correctamente")
    else:
        print("No se encontro la categoria o no hubo cambios")



# Metodo para borrar una categoria
def borrar_categoria():

    id_categoria = int(input("Ingrese el ID de la categoria que desea borrar: "))

    resultado = categorias_fenomeno.delete_one(
        {"_id": id_categoria}
    )

    if resultado.deleted_count > 0:
        print("Categoria borrada correctamente")
    else:
        print("No se encontro la categoria")



# Menu principal de categorias
def menu_categorias():

    while True:

        print("\n===== CRUD CATEGORIAS =====")
        print("1. Insertar categoria")
        print("2. Modificar categoria")
        print("3. Borrar categoria")
        print("4. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            insertar_categoria()

        elif opcion == "2":
            modificar_categoria()

        elif opcion == "3":
            borrar_categoria()

        elif opcion == "4":
            print("Saliendo del programa")
            break

        else:
            print("Opcion incorrecta")
menu_categorias()