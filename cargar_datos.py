# ==========================================================
# PROYECTO RCOFA
# Archivo: carga_datos.py
# Descripción: Conexión a MongoDB y carga inicial de datos.
#Tienen que poner el archivo Ubicaciones.csv dentro de las carpeta del proyecto.
# ==========================================================

# 1. IMPORTACIÓN DE LIBRERÍAS
from pymongo import MongoClient
import csv

# Importamos la función de clasificación desde subrutinas.py
from subrutinas import clasificar_tipo_zona

# 2. CONEXIÓN CON MONGODB
# Dirección de conexión a MongoDB.
MONGO_URI = "mongodb://admin:parda99%2A@127.0.0.1:27017/admin"

# Establecemos la conexión con el servidor MongoDB.
cliente = MongoClient(MONGO_URI)

# Comprobamos que MongoDB esté funcionando.
cliente.admin.command("ping")

print("Conexión con MongoDB exitosa")

# 3. SELECCIÓN DE BASE DE DATOS Y COLECCIONES
# Seleccionamos la base de datos del proyecto.
db = cliente["RCOFA"]

# Creamos las referencias a las colecciones.
ubicaciones = db["ubicaciones"]
categorias_fenomeno = db["categorias_fenomeno"]
observadores = db["observadores"]
avistamientos = db["avistamientos"]


# 4. CARGA DE UBICACIONES
def cargar_ubicaciones():

    # Comprobamos si ya existen localidades.
    if ubicaciones.count_documents({}) > 0:
        print("La colección ya contiene localidades.")
        return

    # Abrimos el archivo CSV.
    # utf-8-sig permite leer correctamente caracteres especiales.
    with open("ubicaciones.csv", "r", encoding="utf-8-sig") as archivo:

        # Leemos el CSV utilizando punto y coma como separador.
        lector = csv.DictReader(archivo, delimiter=";")

        # Mostramos los encabezados encontrados.
        print("Encabezados encontrados:", lector.fieldnames)

        # Lista donde almacenaremos los documentos.
        lista_ubicaciones = []

        # Recorremos cada fila del archivo.
        for fila in lector:

            # Creamos un documento con los datos de la localidad.
            documento = {
                "id_sector": fila["Id"].strip(),
                "provincia": fila["Provincia"].strip(),
                "canton": fila["Cantón"].strip(),
                "distrito": fila["Distrito"].strip(),
                "localidad": (fila["Poblado"] or "").strip(),

                # Clasificamos el tipo de zona.
                "tipo_zona": clasificar_tipo_zona(
                    fila["Provincia"],
                    fila["Cantón"],
                    fila["Poblado"] or ""
                )
            }
            # Agregamos el documento a la lista.
            lista_ubicaciones.append(documento)
        # Insertamos todos los documentos en MongoDB.
        if lista_ubicaciones:
            resultado = ubicaciones.insert_many(lista_ubicaciones)
            print(
                "Localidades insertadas:",
                len(resultado.inserted_ids)
            )
# 5. CARGA DE CATEGORÍAS DE FENÓMENOS
def cargar_categorias():

    # Evitamos insertar categorías duplicadas.
    if categorias_fenomeno.count_documents({}) > 0:
        print("Las categorías ya están registradas.")
        return

    # Definimos las categorías del examen.
    categorias = [
        {
            "_id": 1,
            "nombre": "Luminaria estacionaria",
            "descripcion": "Fenómeno luminoso que permanece aparentemente fijo en el cielo."
        },
        {
            "_id": 2,
            "nombre": "Eco radar no identificado",
            "descripcion": "Señal detectada por radar cuyo origen no ha sido identificado."
        },
        {
            "_id": 3,
            "nombre": "Estela luminosa",
            "descripcion": "Rastro brillante observado desplazándose por el cielo."
        },
        {
            "_id": 4,
            "nombre": "Objeto Volador NO Identificado",
            "descripcion": "Objeto observado en el espacio aéreo cuyo origen es desconocido."
        }
    ]

    # Insertamos cada categoría individualmente.
    for categoria in categorias:

        categorias_fenomeno.insert_one(categoria)

    print("Categorías registradas:", len(categorias))

# 6. CARGA DE OBSERVADORES
def cargar_observadores():
    # Evitamos insertar observadores duplicados.
    if observadores.count_documents({}) > 0:
        print("Los observadores ya están registrados.")
        return

    # Definimos los observadores de ejemplo.
    lista_observadores = [
        {
            "_id": 1,
            "alias_o_estacion": "Observador_Pacifico",
            "rol": "Testigo ciudadano",
            "indice_confiabilidad": 0.85
        },
        {
            "_id": 2,
            "alias_o_estacion": "Radar_Central",
            "rol": "Operador radar",
            "indice_confiabilidad": 0.95
        },
        {
            "_id": 3,
            "alias_o_estacion": "Estacion_Meteorologica_01",
            "rol": "Estación meteorológica",
            "indice_confiabilidad": 0.98
        },
        {
            "_id": 4,
            "alias_o_estacion": "Observador_Cartago",
            "rol": "Testigo ciudadano",
            "indice_confiabilidad": 0.75
        },
        {
            "_id": 5,
            "alias_o_estacion": "Radar_Puntarenas",
            "rol": "Operador radar",
            "indice_confiabilidad": 0.90
        }
    ]

    # Insertamos todos los observadores juntos.
    resultado = observadores.insert_many(lista_observadores)

    print(
        "Observadores registrados:",
        len(resultado.inserted_ids)
    )

# 7. PROGRAMA PRINCIPAL
if __name__ == "__main__":
    try:

        print("\n========== CARGA DE DATOS RCOFA ==========\n")

        # Cargamos las localidades.
        cargar_ubicaciones()

        # Cargamos las categorías.
        cargar_categorias()

        # Cargamos los observadores.
        cargar_observadores()

        print("\n========== RESUMEN DE DATOS ==========\n")

        # Consultamos la cantidad de documentos almacenados.
        print(
            "Total de localidades:",
            ubicaciones.count_documents({})
        )

        print(
            "Total de categorías:",
            categorias_fenomeno.count_documents({})
        )

        print(
            "Total de observadores:",
            observadores.count_documents({})
        )

        print("\nCarga de datos finalizada correctamente.")

    except Exception as error:

        # Mostramos cualquier error durante la ejecución.
        print("Se produjo un error:", error)

    finally:

        # Cerramos la conexión con MongoDB.
        cliente.close()

        print("Conexión cerrada.")