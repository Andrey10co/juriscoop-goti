# ============================================================
#  pbi_creditos_query.py
#  Pegar este script en Power BI Desktop:
#  Inicio → Transformar datos → clic derecho en la tabla →
#  Configuración de origen → reemplazar el script
# ============================================================
import sqlite3
import pandas as pd

DB_PATH = r"C:\Users\Andrey Esteban\OneDrive - Universidad de la Sabana\Documents\GOTI\Proyecto juriscop entregas\Entrega proyecto juriscoop- segundo corte\Pipeline\juriscoop.db"

# Python usado: C:\Users\Andrey Esteban\AppData\Local\Python\pythoncore-3.14-64

_conn = sqlite3.connect(DB_PATH)

solicitudes_credito = pd.read_sql("SELECT * FROM solicitudes_credito", _conn)
etapas_proceso      = pd.read_sql("SELECT * FROM etapas_proceso",      _conn)
empleados           = pd.read_sql("SELECT * FROM empleados",           _conn)

_conn.close()
del _conn
