# ============================================================
#  pbi_cartera_query.py
#  Pegar este script en Power BI Desktop:
#  Inicio → Obtener datos → Más → Otro → Script de Python
# ============================================================
import sqlite3
import pandas as pd
import json

DB_PATH = r"C:\Users\Andrey Esteban\OneDrive - Universidad de la Sabana\Documents\GOTI\Proyecto juriscop entregas\Entrega proyecto juriscoop- segundo corte\Pipeline\juriscoop.db"

# Python usado: C:\Users\Andrey Esteban\AppData\Local\Python\pythoncore-3.14-64

conn = sqlite3.connect(DB_PATH)
# Solo el último corte disponible (evita duplicados cuando hay cargas históricas)
_raw = pd.read_sql(
    """SELECT id, fecha_corte, archivo_origen, datos_json, fecha_carga
       FROM cartera_raw
       WHERE fecha_corte = (SELECT MAX(fecha_corte) FROM cartera_raw)""",
    conn
)
conn.close()

_expandido = _raw["datos_json"].apply(json.loads).apply(pd.Series)
cartera = pd.concat(
    [_raw[["id", "fecha_corte", "archivo_origen", "fecha_carga"]], _expandido],
    axis=1
)

# Convertir columnas numéricas
for col in ["Saldo_Capital", "Saldo_Interes", "Tasa_Interes_Anual",
            "Cuota_Mensual", "Numero_Cuotas_Pendientes", "Dias_Mora"]:
    if col in cartera.columns:
        cartera[col] = pd.to_numeric(cartera[col], errors="coerce")

# Convertir fechas
for col in ["Fecha_Desembolso", "Fecha_Vencimiento", "Fecha_Corte"]:
    if col in cartera.columns:
        cartera[col] = pd.to_datetime(cartera[col], errors="coerce")

# Limpiar variables intermedias para que Power BI no las cargue como tablas
del _raw, _expandido
