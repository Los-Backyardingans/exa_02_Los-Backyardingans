"""
avistamientos.py
"""

import random
from datetime import datetime, timedelta
from subrutinas import generar_codigo_reporte

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

    documentos = []
    for n in range(1, cantidad + 1):
        ubi = random.choice(ubicaciones)      # localidad real al azar
        codigo = generar_codigo_reporte(n)    # REP-00000001, REP-00000002...

        # Campos que SIEMPRE existen
        doc = {
            "_id": codigo,
            "codigo_reporte": codigo,
            "fecha_evento": inicio + timedelta(seconds=random.randint(0, rango_seg)),
            "id_categoria": random.choice(ids_categoria),
            "ubicacion": {
                "id_sector": ubi["id_sector"],
                "provincia": ubi["provincia"],   # ajuste a los nombres de su CSV
                "canton": ubi["canton"],
                "localidad": ubi["localidad"],
            },
        }

        # Campos OPCIONALES (por eso los documentos no son uniformes)
        if random.random() < 0.90:
            doc["duracion_seg"] = random.randint(5, 600)
        if random.random() < 0.85:
            doc["id_observador"] = random.choice(ids_observador)
        if random.random() < 0.70:
            doc["ubicacion"]["distrito"] = ubi["distrito"]
        if random.random() < 0.60:
            tele = {}
            if random.random() < 0.8:
                tele["visibilidad_km"] = round(random.uniform(0.5, 30.0), 1)
            if random.random() < 0.8:
                tele["nubosidad_pct"] = random.randint(0, 100)
            if random.random() < 0.8:
                tele["viento_nudos"] = round(random.uniform(0.0, 40.0), 1)
            if tele:
                doc["telemetria_entorno"] = tele

        documentos.append(doc)

    bd.avistamientos.insert_many(documentos)
    print(f"Avistamientos generados: {len(documentos)}")